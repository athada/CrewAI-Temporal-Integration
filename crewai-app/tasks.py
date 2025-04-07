from typing import Tuple, List, Any
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