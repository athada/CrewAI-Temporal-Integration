import os
import socket
import asyncio
import time
from datetime import timedelta
from temporalio.client import Client as TemporalClient
from temporalio.worker import Worker

# Import agent config and components from other modules
from agents import AgentConfig
from workflows import CollaborativeAgentWorkflow

# Import all activities
from agents import (setup_researcher_agent, setup_writer_agent, setup_critic_agent, 
                   setup_integrator_agent, agent_response_to_feedback, resolve_agent_disagreement)
from thinking import (researcher_detailed_thinking, writer_detailed_thinking, 
                     researcher_think, writer_think)
from tasks import (researcher_perform_research, writer_create_report, 
                  collaborative_research, collaborative_report_writing)
from messages import (send_message, ask_question, provide_answer, make_proposal, 
                     provide_feedback, get_conversation_history, collaborate_on_decision)

# Flag to control whether to use Temporal
use_temporal = True  # Set to True to use Temporal, False to run directly
use_collaborative_mode = True  # Set to True to use the collaborative workflow

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
    
    # Define the tasks for our agents
    research_topic = "Integration of Temporal with AI systems"
    report_title = "Benefits of Temporal for AI Workflows"
    
    # Use the collaborative workflow
    task_queue = "collaborative-agent-queue"
    
    print(f"Starting Temporal worker on task queue: {task_queue}")
    async with Worker(
        client=client,
        task_queue=task_queue,
        workflows=[CollaborativeAgentWorkflow],
        activities=[
            # Agent activities
            setup_researcher_agent,
            setup_writer_agent,
            setup_critic_agent, 
            setup_integrator_agent,
            agent_response_to_feedback,
            resolve_agent_disagreement,
            
            # Thinking activities
            researcher_detailed_thinking,
            writer_detailed_thinking,
            researcher_think,
            writer_think,
            
            # Task activities
            researcher_perform_research,
            writer_create_report,
            collaborative_research,
            collaborative_report_writing,
            
            # Communication activities
            send_message,
            ask_question,
            provide_answer,
            make_proposal,
            provide_feedback,
            get_conversation_history,
            collaborate_on_decision,
        ],
    ):
        print("Executing collaborative agent workflow")
        result = await client.execute_workflow(
            CollaborativeAgentWorkflow.run,
            args=[research_topic, report_title],
            id=f"collaborative-agent-workflow-{int(time.time())}",
            task_queue=task_queue,
        )
        
        print(f"\nWorkflow result summary:")
        print(f"Final report length: {len(result['final_report'])} characters")
        print(f"Total thinking steps: {result['collaborative_process']['thinking_steps']}")
        print(f"Team members: {', '.join(result['team'].values())}")
        
        return result

if __name__ == "__main__":
    if use_temporal:
        # Run with Temporal
        print("Running with Temporal orchestration")
        asyncio.run(main_temporal())
    else:
        # Run without Temporal
        run_without_temporal() 