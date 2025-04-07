from datetime import timedelta
from temporalio import workflow
from typing import Dict, Any, List

@workflow.defn
class CollaborativeAgentWorkflow:
    @workflow.run
    async def run(self, research_topic: str, report_title: str) -> Dict[str, Any]:
        # Import activities only within workflow methods to avoid sandbox issues
        from agents import (setup_researcher_agent, setup_writer_agent, 
                           setup_critic_agent, setup_integrator_agent,
                           agent_response_to_feedback, resolve_agent_disagreement)
        from tasks import (collaborative_research, collaborative_report_writing)
        from thinking import researcher_detailed_thinking, writer_detailed_thinking
        from messages import (ask_question, provide_answer, make_proposal, 
                             provide_feedback, get_conversation_history)
        
        # Store all thinking and conversation data
        all_thinking = []
        all_conversations = []
        
        # Initialize the agents
        researcher = await workflow.execute_activity(
            setup_researcher_agent,
            start_to_close_timeout=timedelta(seconds=30),
        )
        print(f"Initialized {researcher.name} agent in workflow")
        
        writer = await workflow.execute_activity(
            setup_writer_agent,
            start_to_close_timeout=timedelta(seconds=30),
        )
        print(f"Initialized {writer.name} agent in workflow")
        
        critic = await workflow.execute_activity(
            setup_critic_agent,
            start_to_close_timeout=timedelta(seconds=30),
        )
        print(f"Initialized {critic.name} agent in workflow")
        
        integrator = await workflow.execute_activity(
            setup_integrator_agent,
            start_to_close_timeout=timedelta(seconds=30),
        )
        print(f"Initialized {integrator.name} agent in workflow")
        
        # STAGE 1: PLANNING - Integrator coordinates the team
        print(f"\n{'='*20} PLANNING PHASE: TEAM COORDINATION {'='*20}\n")
        
        # Integrator asks each agent about their approach
        planning_question_to_researcher = await workflow.execute_activity(
            ask_question,
            args=[integrator, researcher, f"How would you approach researching {research_topic}?"],
            start_to_close_timeout=timedelta(seconds=10),
        )
        
        researcher_plan_response = await workflow.execute_activity(
            provide_answer,
            args=[
                researcher, 
                integrator, 
                f"I would start by identifying key features of Temporal relevant to AI workflows, then research specific use cases and implementation patterns.",
                planning_question_to_researcher["message_id"],
                planning_question_to_researcher["conversation_id"]
            ],
            start_to_close_timeout=timedelta(seconds=10),
        )
        
        planning_question_to_writer = await workflow.execute_activity(
            ask_question,
            args=[integrator, writer, f"How would you structure a report on {report_title}?"],
            start_to_close_timeout=timedelta(seconds=10),
        )
        
        writer_plan_response = await workflow.execute_activity(
            provide_answer,
            args=[
                writer, 
                integrator, 
                f"I'd recommend an executive summary, detailed findings, implementation guide, and business impact sections to make it accessible to different audiences.",
                planning_question_to_writer["message_id"],
                planning_question_to_writer["conversation_id"]
            ],
            start_to_close_timeout=timedelta(seconds=10),
        )
        
        # Integrator proposes a project plan
        project_plan_proposal = await workflow.execute_activity(
            make_proposal,
            args=[
                integrator,
                [researcher, writer, critic],  # Send to all team members
                f"Based on our discussions, I propose the following plan: 1) Collaborative research led by the Researcher with Critic input, 2) Draft report creation by Writer, 3) Critical review by Critic, 4) Final integration and revisions led by me. Timeline: 2 days for research, 2 days for writing, 1 day for review, 1 day for integration."
            ],
            start_to_close_timeout=timedelta(seconds=15),
        )
        
        # Get feedback from team members
        critic_feedback = await workflow.execute_activity(
            provide_feedback,
            args=[
                critic,
                integrator,
                "The timeline seems tight for thorough research. I suggest allocating 3 days for research and reducing integration to half a day.",
                project_plan_proposal["message_id"],
                project_plan_proposal["conversation_id"]
            ],
            start_to_close_timeout=timedelta(seconds=10),
        )
        
        # Resolve disagreement on timeline
        resolution = await workflow.execute_activity(
            resolve_agent_disagreement,
            args=[
                [integrator, critic],
                "Project timeline",
                [
                    "2 days for research is sufficient given the scope",
                    "3 days for research is needed for thorough investigation"
                ]
            ],
            start_to_close_timeout=timedelta(seconds=15),
        )
        
        # STAGE 2: COLLABORATIVE RESEARCH
        print(f"\n{'='*20} COLLABORATIVE RESEARCH PHASE {'='*20}\n")
        
        # Conduct collaborative research with all agents
        research_result, research_thinking, research_conversation_id = await workflow.execute_activity(
            collaborative_research,
            args=[researcher, [critic, integrator], research_topic],
            start_to_close_timeout=timedelta(minutes=5),
        )
        
        # Log each detailed thinking step from research
        for thinking_step in research_thinking:
            thinking_record = await workflow.execute_activity(
                researcher_detailed_thinking,
                args=[researcher, thinking_step],
                start_to_close_timeout=timedelta(seconds=10),
            )
            all_thinking.append(thinking_record)
        
        # Get the conversation history from the research phase
        research_conversation = await workflow.execute_activity(
            get_conversation_history,
            args=[research_conversation_id],
            start_to_close_timeout=timedelta(seconds=10),
        )
        all_conversations.append({"phase": "research", "conversation": research_conversation})
        
        # STAGE 3: COLLABORATIVE WRITING
        print(f"\n{'='*20} COLLABORATIVE WRITING PHASE {'='*20}\n")
        
        # Writer creates report with collaboration from other agents
        final_report, writing_thinking, writing_conversation_id = await workflow.execute_activity(
            collaborative_report_writing,
            args=[writer, [researcher, critic, integrator], report_title, research_result],
            start_to_close_timeout=timedelta(minutes=5),
        )
        
        # Log each detailed thinking step from writing
        for thinking_step in writing_thinking:
            thinking_record = await workflow.execute_activity(
                writer_detailed_thinking,
                args=[writer, thinking_step],
                start_to_close_timeout=timedelta(seconds=10),
            )
            all_thinking.append(thinking_record)
        
        # Get the conversation history from the writing phase
        writing_conversation = await workflow.execute_activity(
            get_conversation_history,
            args=[writing_conversation_id],
            start_to_close_timeout=timedelta(seconds=10),
        )
        all_conversations.append({"phase": "writing", "conversation": writing_conversation})
        
        # STAGE 4: FINAL REVIEW AND FEEDBACK
        print(f"\n{'='*20} FINAL REVIEW PHASE {'='*20}\n")
        
        # Critic provides final feedback on the report
        final_feedback_message = await workflow.execute_activity(
            provide_feedback,
            args=[
                critic,
                writer,
                "The report is comprehensive but could use more specific implementation examples in the recommendations section.",
                "final_report",  # Treating the report itself as the "message" being responded to
                writing_conversation_id
            ],
            start_to_close_timeout=timedelta(seconds=15),
        )
        
        # Writer responds to feedback
        writer_response = await workflow.execute_activity(
            agent_response_to_feedback,
            args=[
                writer,
                final_feedback_message["content"],
                report_title
            ],
            start_to_close_timeout=timedelta(seconds=15),
        )
        
        # Print thinking summary
        print(f"\n{'='*20} COLLABORATION SUMMARY {'='*20}")
        print(f"Total thinking steps recorded: {len(all_thinking)}")
        print(f"Research thinking steps: {len(research_thinking)}")
        print(f"Writing thinking steps: {len(writing_thinking)}")
        print(f"Total conversations: {len(all_conversations)}")
        print(f"Total messages exchanged: {sum(len(conv['conversation']) for conv in all_conversations if 'conversation' in conv)}")
        
        # Return comprehensive results
        result = {
            "final_report": final_report,
            "collaborative_process": {
                "thinking_steps": len(all_thinking),
                "conversations": all_conversations,
                "research_conversation_id": research_conversation_id,
                "writing_conversation_id": writing_conversation_id,
                "final_feedback": final_feedback_message["content"],
                "writer_response": writer_response
            },
            "team": {
                "researcher": researcher.name,
                "writer": writer.name,
                "critic": critic.name,
                "integrator": integrator.name
            }
        }
        
        return result 