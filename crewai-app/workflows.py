from datetime import timedelta
from temporalio import workflow
from typing import Dict, Any, List

@workflow.defn
class DetailedThinkingWorkflow:
    @workflow.run
    async def run(self, research_topic: str, report_title: str) -> str:
        # Import activities only within workflow methods to avoid sandbox issues
        from agents import setup_researcher_agent, setup_writer_agent
        from tasks import researcher_perform_research, writer_create_report
        from thinking import researcher_detailed_thinking, writer_detailed_thinking
        
        # Store all thinking for analysis
        all_thinking = []
        
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
        
        # RESEARCHER WORK WITH DETAILED THINKING
        print(f"\n{'='*20} RESEARCHER AGENT THINKING PROCESS {'='*20}\n")
        
        # Perform research with detailed thinking
        research_result, research_thinking = await workflow.execute_activity(
            researcher_perform_research,
            args=[researcher, research_topic],
            start_to_close_timeout=timedelta(minutes=5),
        )
        
        # Log each detailed thinking step
        for thinking_step in research_thinking:
            thinking_record = await workflow.execute_activity(
                researcher_detailed_thinking,
                args=[researcher, thinking_step],
                start_to_close_timeout=timedelta(seconds=10),
            )
            all_thinking.append(thinking_record)
        
        print(f"\nResearch completed with {len(research_thinking)} thinking steps")
        print(f"Research findings length: {len(research_result)} characters")
        
        # WRITER WORK WITH DETAILED THINKING
        print(f"\n{'='*20} WRITER AGENT THINKING PROCESS {'='*20}\n")
        
        # Writer creates report with detailed thinking
        final_report, writing_thinking = await workflow.execute_activity(
            writer_create_report,
            args=[writer, report_title, research_result],
            start_to_close_timeout=timedelta(minutes=5),
        )
        
        # Log each detailed thinking step
        for thinking_step in writing_thinking:
            thinking_record = await workflow.execute_activity(
                writer_detailed_thinking,
                args=[writer, thinking_step],
                start_to_close_timeout=timedelta(seconds=10),
            )
            all_thinking.append(thinking_record)
        
        print(f"\nReport writing completed with {len(writing_thinking)} thinking steps")
        print(f"Final report length: {len(final_report)} characters")
        
        # Print thinking summary
        print(f"\n{'='*20} THINKING SUMMARY {'='*20}")
        print(f"Total thinking steps recorded: {len(all_thinking)}")
        print(f"Researcher thinking steps: {len(research_thinking)}")
        print(f"Writer thinking steps: {len(writing_thinking)}")
        
        # Return the final report
        return final_report 