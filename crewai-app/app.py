import os
import socket
import asyncio
import time
from datetime import timedelta
from temporalio.client import Client as TemporalClient
from temporalio.worker import Worker

# Import agent config and components from other modules
from agents import AgentConfig
from workflows import DetailedThinkingWorkflow

# Import all activities
from agents import setup_researcher_agent, setup_writer_agent
from thinking import researcher_detailed_thinking, writer_detailed_thinking, researcher_think, writer_think
from tasks import researcher_perform_research, writer_create_report

# Flag to control whether to use Temporal
use_temporal = True  # Set to True to use Temporal, False to run directly

# Function to run without Temporal - direct execution
def run_without_temporal():
    print("Running without Temporal orchestration")
    
    # Create agents directly
    researcher = AgentConfig(
        name="Researcher",
        role="Research Expert",
        goal="Research the latest AI technologies",
        backstory="You are an AI research expert"
    )
    
    writer = AgentConfig(
        name="Writer",
        role="Technical Writer",
        goal="Communicate complex AI concepts clearly",
        backstory="You specialize in technical writing"
    )
    
    # Simulate research with thinking
    print(f"🧠 {researcher.name} is thinking: I need to understand Temporal integration with AI")
    print(f"🧠 {researcher.name} is thinking: I should look at reliability features")
    print(f"Agent '{researcher.name}' is researching...")
    research_findings = "Research on Temporal with AI has been completed."
    
    # Simulate writing with thinking
    print(f"🧠 {writer.name} is thinking: I need to structure this report carefully")
    print(f"🧠 {writer.name} is thinking: I should highlight the key benefits")
    print(f"Agent '{writer.name}' is writing...")
    report = f"Report by {writer.name}: Temporal integration with AI is valuable."
    
    result = f"Process completed:\n{report}\nBased on: {research_findings}"
    print(f"Final result: {result}")
    return result

# Main function to start the workflow with Temporal
async def main_temporal():
    temporal_host = os.environ.get("TEMPORAL_HOST", "temporal")
    temporal_port = os.environ.get("TEMPORAL_PORT", "7233")
    
    print(f"Connecting to Temporal at {temporal_host}:{temporal_port}")
    client = await TemporalClient.connect(f"{temporal_host}:{temporal_port}")
    
    task_queue = "detailed-thinking-queue"
    
    # Define the tasks for our agents
    research_topic = "Integration of Temporal with AI systems"
    report_title = "Benefits of Temporal for AI Workflows"
    
    print(f"Starting Temporal worker on task queue: {task_queue}")
    async with Worker(
        client=client,
        task_queue=task_queue,
        workflows=[DetailedThinkingWorkflow],
        activities=[
            setup_researcher_agent,
            setup_writer_agent,
            researcher_detailed_thinking,
            writer_detailed_thinking,
            researcher_think,
            writer_think,
            researcher_perform_research,
            writer_create_report,
        ],
    ):
        print("Executing workflow with detailed thinking tracking")
        result = await client.execute_workflow(
            DetailedThinkingWorkflow.run,
            args=[research_topic, report_title],
            id=f"detailed-thinking-workflow-{int(time.time())}",
            task_queue=task_queue,
        )
        
        print(f"\nWorkflow result:\n{result}")
        return result

if __name__ == "__main__":
    if use_temporal:
        # Run with Temporal
        print("Running with Temporal orchestration")
        asyncio.run(main_temporal())
    else:
        # Run without Temporal
        run_without_temporal() 