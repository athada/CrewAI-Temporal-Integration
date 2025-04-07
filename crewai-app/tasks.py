from typing import Tuple, List, Any, Optional
import asyncio
from temporalio import activity
from agents import AgentConfig
from thinking import ThinkingStep

@activity.defn
async def researcher_perform_research(agent: Any, task: str) -> Tuple[str, List[ThinkingStep]]:
    """The researcher agent performs research with detailed thinking steps"""
    # Handle both AgentConfig objects and dictionaries
    agent_name = agent["name"] if isinstance(agent, dict) else agent.name
    
    print(f"Agent '{agent_name}' is researching: {task}")
    
    # Create detailed thinking steps that show the reasoning process
    thinking_steps = [
        ThinkingStep(
            content="I need to understand what Temporal is and how it integrates with AI systems",
            step_number=1,
            reasoning="To provide valuable research, I must first understand both technologies",
            evidence=["Temporal is a workflow orchestration platform", "AI systems often need robust workflow management"],
            conclusion="Research should focus on workflow orchestration for AI tasks"
        ),
        ThinkingStep(
            content="Identifying the key benefits Temporal provides specifically for AI workflows",
            step_number=2,
            reasoning="AI workflows have unique characteristics that benefit from Temporal's features",
            evidence=[
                "AI tasks can be long-running", 
                "Models may need to be retrained periodically", 
                "Error handling is critical for AI pipelines"
            ],
            conclusion="Durability, reliability, and error handling are key advantages"
        ),
        ThinkingStep(
            content="Examining use cases where Temporal solves AI-specific challenges",
            step_number=3,
            reasoning="Concrete examples will make the research more applicable",
            evidence=[
                "ML model training often requires complex orchestration",
                "AI inference pipelines need monitoring and observability",
                "Data preprocessing for AI can be complex and error-prone"
            ],
            conclusion="Temporal provides solutions for the entire AI lifecycle"
        ),
    ]
    
    # Simulate actual work
    for step in thinking_steps:
        await asyncio.sleep(1)  # Simulate thinking time
    
    # Create the research findings based on the thinking steps
    result = f"Research findings on {task} by {agent_name}:\n\n"
    result += "1. Temporal provides durability and reliability for AI workflows:\n"
    result += "   - Automatic retries for failed operations\n"
    result += "   - State persistence across system failures\n"
    result += "   - Versioning support for evolving AI models\n\n"
    
    result += "2. Temporal enables complex AI orchestration:\n"
    result += "   - Coordination of distributed training jobs\n"
    result += "   - Management of data preprocessing pipelines\n"
    result += "   - Scheduling of model evaluation and retraining\n\n"
    
    result += "3. Benefits for production AI systems:\n"
    result += "   - Enhanced observability through workflow history\n"
    result += "   - Simplified debugging of complex AI pipelines\n"
    result += "   - Scalable architecture for growing AI workloads"
    
    print(f"Agent '{agent_name}' completed research with {len(thinking_steps)} thinking steps")
    return (result, thinking_steps)

@activity.defn
async def writer_create_report(agent: Any, task: str, research_findings: str) -> Tuple[str, List[ThinkingStep]]:
    """The writer agent creates a report with detailed thinking steps"""
    # Handle both AgentConfig objects and dictionaries
    agent_name = agent["name"] if isinstance(agent, dict) else agent.name
    
    print(f"Agent '{agent_name}' is writing: {task}")
    print(f"Using research: {research_findings[:100]}...")
    
    # Create detailed thinking steps for the writing process
    thinking_steps = [
        ThinkingStep(
            content="Planning the structure of the report for maximum clarity",
            step_number=1,
            reasoning="A well-structured report helps readers understand complex technical topics",
            evidence=[
                "Technical reports need clear sections",
                "Starting with an executive summary helps busy readers",
                "The audience may have varying levels of technical knowledge"
            ],
            conclusion="Will use executive summary, findings, and recommendations structure"
        ),
        ThinkingStep(
            content="Analyzing the research findings to extract key points",
            step_number=2,
            reasoning="Need to transform technical details into digestible insights",
            evidence=[
                "The research highlights durability and reliability benefits",
                "Complex orchestration capabilities are emphasized",
                "Production benefits need to be contextualized for business value"
            ],
            conclusion="Will focus on three main benefit categories with supporting details"
        ),
        ThinkingStep(
            content="Formulating implementation recommendations based on findings",
            step_number=3,
            reasoning="Practical next steps add value beyond just information",
            evidence=[
                "Research suggests Temporal works well for different AI workflows",
                "Implementation complexity varies by use case",
                "Organizations may need to start with smaller projects"
            ],
            conclusion="Will provide a phased implementation approach with concrete steps"
        ),
        ThinkingStep(
            content="Planning the conclusion to emphasize long-term value",
            step_number=4,
            reasoning="Need to connect technical capabilities to business outcomes",
            evidence=[
                "Reliability translates to cost savings",
                "Better orchestration means faster time to market",
                "Observability improves operational efficiency"
            ],
            conclusion="Will emphasize ROI and competitive advantages in conclusion"
        ),
    ]
    
    # Simulate actual writing work
    for step in thinking_steps:
        await asyncio.sleep(1)  # Simulate thinking time
    
    # Create the report based on the thinking steps
    report = f"REPORT: {task.upper()}\n"
    report += f"Prepared by: {agent_name}\n\n"
    
    report += "EXECUTIVE SUMMARY\n"
    report += "This report outlines how Temporal can be integrated with AI systems to enhance reliability, "
    report += "enable complex workflow orchestration, and improve production operations. Our analysis shows "
    report += "that organizations implementing Temporal for AI workflows can expect improved development "
    report += "velocity, reduced operational failures, and better visibility into their AI systems.\n\n"
    
    report += "FINDINGS\n"
    report += "Based on our research:\n"
    report += research_findings + "\n\n"
    
    report += "IMPLEMENTATION RECOMMENDATIONS\n"
    report += "1. Start with a pilot project: Choose a non-critical AI workflow to implement with Temporal\n"
    report += "2. Develop workflow patterns: Create reusable patterns for common AI tasks\n"
    report += "3. Integrate monitoring: Leverage Temporal's visibility tools for operational insights\n"
    report += "4. Scale gradually: Expand to more critical AI systems as your team gains experience\n\n"
    
    report += "CONCLUSION\n"
    report += "Temporal provides significant advantages for AI systems at scale. Organizations that adopt this "
    report += "technology can expect more reliable AI operations, faster development cycles, and better "
    report += "visibility into complex workflows. We recommend proceeding with implementation following "
    report += "the phased approach outlined in this report."
    
    print(f"Agent '{agent_name}' completed writing report with {len(thinking_steps)} thinking steps")
    return (report, thinking_steps)

@activity.defn
async def collaborative_research(primary_agent: Any, supporting_agents: List[Any], 
                                task: str, conversation_id: Optional[str] = None) -> Tuple[str, List[ThinkingStep], str]:
    """Conduct research with collaboration between multiple agents"""
    # Extract the primary agent's name
    primary_name = primary_agent["name"] if isinstance(primary_agent, dict) else primary_agent.name
    
    # Extract supporting agent names
    supporting_names = [agent["name"] if isinstance(agent, dict) else agent.name 
                         for agent in supporting_agents]
    
    print(f"Starting collaborative research led by {primary_name} with support from {', '.join(supporting_names)}")
    
    # Import collaboration activities
    from messages import ask_question, provide_answer, collaborate_on_decision
    
    # Initialize collaborative research
    if conversation_id is None:
        # Create a collaboration record
        collaboration = await collaborate_on_decision(
            agents=[primary_agent] + supporting_agents,
            topic=f"Research on {task}",
            initial_proposal=f"Let's divide the research on {task} into subtopics"
        )
        conversation_id = collaboration["collaboration_id"]
    
    # Simulate collaborative thinking process
    thinking_steps = [
        ThinkingStep(
            content="I need to coordinate with other agents to divide the research tasks",
            step_number=1,
            reasoning="Complex research benefits from diverse expertise and perspectives",
            evidence=["The topic spans multiple knowledge domains", 
                     "Different agents have different specializations"],
            conclusion="Will propose a division of research responsibilities"
        ),
        ThinkingStep(
            content="Analyzing feedback from supporting agents on research approach",
            step_number=2,
            reasoning="Integrating different viewpoints leads to more comprehensive research",
            evidence=["Critic agent highlighted gaps in initial approach",
                     "Writer agent suggested focusing on practical applications"],
            conclusion="Adjusted research focus based on collaborative input"
        ),
        ThinkingStep(
            content="Synthesizing findings from all contributing agents",
            step_number=3,
            reasoning="Need to create a coherent narrative from multiple contributions",
            evidence=["Received specialized input on technical aspects",
                     "Got feedback on explanatory clarity",
                     "Integrator agent provided framework for combining insights"],
            conclusion="Will organize findings into a structured knowledge base"
        ),
    ]
    
    # Simulate collaboration with questions and answers
    # Ask question to a supporting agent
    question = await ask_question(
        sender=primary_agent,
        recipient=supporting_agents[0],
        question=f"What specific aspects of {task} should we prioritize in our research?",
        conversation_id=conversation_id
    )
    
    # Get answer from supporting agent
    answer = await provide_answer(
        sender=supporting_agents[0],
        recipient=primary_agent,
        answer=f"Based on current trends, we should focus on scalability and error handling aspects of {task}.",
        question_message_id=question["message_id"],
        conversation_id=conversation_id
    )
    
    # Simulate research work based on the collaboration
    await asyncio.sleep(2)  # Simulate time spent on research
    
    # Create the collaborative research results
    result = f"Collaborative Research Findings on {task}:\n\n"
    result += f"Led by: {primary_name} with contributions from {', '.join(supporting_names)}\n\n"
    
    result += "1. Temporal provides durability and reliability for AI workflows:\n"
    result += "   - Automatic retries for failed operations (validated by Critic)\n"
    result += "   - State persistence across system failures (researched by Researcher)\n"
    result += "   - Versioning support for evolving AI models (added by Integrator)\n\n"
    
    result += "2. Temporal enables complex AI orchestration:\n"
    result += "   - Coordination of distributed training jobs\n"
    result += "   - Management of data preprocessing pipelines\n"
    result += "   - Scheduling of model evaluation and retraining\n\n"
    
    result += "3. Benefits for production AI systems:\n"
    result += "   - Enhanced observability through workflow history\n"
    result += "   - Simplified debugging of complex AI pipelines\n"
    result += "   - Scalable architecture for growing AI workloads\n\n"
    
    result += "4. Implementation considerations (contributed by multiple agents):\n"
    result += "   - Start with small, non-critical workflows\n"
    result += "   - Develop standardized patterns for common AI tasks\n"
    result += "   - Plan for observability from the beginning"
    
    print(f"Collaborative research completed with {len(thinking_steps)} thinking steps")
    return (result, thinking_steps, conversation_id)

@activity.defn
async def collaborative_report_writing(primary_agent: Any, supporting_agents: List[Any],
                                      task: str, research_findings: str,
                                      conversation_id: Optional[str] = None) -> Tuple[str, List[ThinkingStep], str]:
    """Write a report collaboratively between multiple agents"""
    # Extract the primary agent's name
    primary_name = primary_agent["name"] if isinstance(primary_agent, dict) else primary_agent.name
    
    # Extract supporting agent names
    supporting_names = [agent["name"] if isinstance(agent, dict) else agent.name 
                         for agent in supporting_agents]
    
    print(f"Starting collaborative writing led by {primary_name} with support from {', '.join(supporting_names)}")
    
    # Import collaboration activities
    from messages import send_message, make_proposal, provide_feedback
    
    # Initialize collaborative writing
    if conversation_id is None:
        # Create a new conversation for this collaboration
        from messages import collaborate_on_decision
        collaboration = await collaborate_on_decision(
            agents=[primary_agent] + supporting_agents,
            topic=f"Writing report on {task}",
            initial_proposal=f"Let's create a comprehensive report on {task} with different sections"
        )
        conversation_id = collaboration["collaboration_id"]
    
    # Simulate collaborative thinking process
    thinking_steps = [
        ThinkingStep(
            content="Planning the collaborative writing process",
            step_number=1,
            reasoning="Complex reports benefit from diverse expertise and writing styles",
            evidence=["Different sections require different expertise", 
                     "Review process improves quality"],
            conclusion="Will assign different sections to different agents"
        ),
        ThinkingStep(
            content="Developing the report structure based on research",
            step_number=2,
            reasoning="A clear structure makes the report more accessible and logical",
            evidence=["Research contains distinct categories of findings",
                     "Executive summary needs to highlight key points"],
            conclusion="Created a four-part structure with executive summary"
        ),
        ThinkingStep(
            content="Integrating feedback from multiple reviewers",
            step_number=3,
            reasoning="Constructive criticism improves clarity and accuracy",
            evidence=["Critic agent identified technical inconsistencies",
                     "Researcher suggested adding more technical details",
                     "Integrator provided feedback on overall flow"],
            conclusion="Made revisions to improve technical accuracy and readability"
        ),
        ThinkingStep(
            content="Finalizing the report with consensus from all agents",
            step_number=4,
            reasoning="Final version should represent agreed-upon content and style",
            evidence=["Held final review session with all agents",
                     "Addressed all outstanding comments",
                     "Balanced technical depth with accessibility"],
            conclusion="Produced a final report that meets all objectives"
        ),
    ]
    
    # Simulate collaborative writing with proposals and feedback
    # Make initial proposal about report structure
    proposal = await make_proposal(
        sender=primary_agent,
        recipient=supporting_agents[0],
        proposal=f"I propose structuring the report with: Executive Summary, Technical Findings, Implementation Guide, and Business Impact sections.",
        conversation_id=conversation_id
    )
    
    # Get feedback on the proposal
    feedback = await provide_feedback(
        sender=supporting_agents[0],
        recipient=primary_agent,
        feedback="The structure looks good, but I suggest adding a 'Challenges and Limitations' section to provide a balanced view.",
        proposal_message_id=proposal["message_id"],
        conversation_id=conversation_id
    )
    
    # Additional exchanges between agents
    await send_message(
        sender=supporting_agents[1] if len(supporting_agents) > 1 else supporting_agents[0],
        recipient=primary_agent,
        content="I've drafted the Technical Findings section. Please review and let me know if you need any changes.",
        message_type="update",
        conversation_id=conversation_id
    )
    
    # Simulate writing work
    await asyncio.sleep(3)  # Simulate collaborative writing time
    
    # Create the collaborative report
    report = f"COLLABORATIVE REPORT: {task.upper()}\n"
    report += f"Primary Author: {primary_name} with contributions from {', '.join(supporting_names)}\n\n"
    
    report += "EXECUTIVE SUMMARY\n"
    report += "This collaboratively developed report outlines how Temporal can be integrated with AI systems to enhance reliability, "
    report += "enable complex workflow orchestration, and improve production operations. Our multi-agent analysis shows "
    report += "that organizations implementing Temporal for AI workflows can expect improved development "
    report += "velocity, reduced operational failures, and better visibility into their AI systems.\n\n"
    
    report += "TECHNICAL FINDINGS\n"
    report += "Based on our collaborative research:\n"
    report += research_findings + "\n\n"
    
    report += "IMPLEMENTATION RECOMMENDATIONS\n"
    report += "1. Start with a pilot project: Choose a non-critical AI workflow to implement with Temporal\n"
    report += "2. Develop workflow patterns: Create reusable patterns for common AI tasks\n"
    report += "3. Integrate monitoring: Leverage Temporal's visibility tools for operational insights\n"
    report += "4. Scale gradually: Expand to more critical AI systems as your team gains experience\n\n"
    
    report += "CHALLENGES AND LIMITATIONS\n"  # Added based on feedback
    report += "1. Learning curve: Teams may need time to adapt to the Temporal programming model\n"
    report += "2. Initial setup: Establishing proper monitoring and alerting requires upfront investment\n"
    report += "3. Integration complexity: Existing systems may need adapters or modifications\n\n"
    
    report += "BUSINESS IMPACT\n"
    report += "1. Reduced downtime through improved error handling and recovery\n"
    report += "2. Lower operational costs through automation and efficient resource usage\n"
    report += "3. Faster time-to-market for AI features through reliable orchestration\n\n"
    
    report += "CONCLUSION\n"
    report += "Through our collaborative analysis, we've determined that Temporal provides significant advantages for AI systems at scale. "
    report += "Organizations that adopt this technology can expect more reliable AI operations, faster development cycles, and better "
    report += "visibility into complex workflows. We recommend proceeding with implementation following "
    report += "the phased approach outlined in this report."
    
    print(f"Collaborative writing completed with {len(thinking_steps)} thinking steps")
    return (report, thinking_steps, conversation_id) 