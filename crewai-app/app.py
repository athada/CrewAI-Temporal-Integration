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

# Define the communication adjacency matrix as a sparse matrix (dictionary)
# Keys are (sender, recipient) tuples, values are 0-1 (0=no communication, 1=allowed)
COMMUNICATION_MATRIX = {
    # Researcher can communicate with Writer and Integrator, but not directly with Critic
    ("Researcher", "Writer"): 1.0,
    ("Researcher", "Integrator"): 1.0,
    ("Researcher", "Critic"): 0.0,
    
    # Writer can communicate with everyone
    ("Writer", "Researcher"): 0.8,
    ("Writer", "Critic"): 1.0,
    ("Writer", "Integrator"): 1.0,
    
    # Critic can communicate with Writer and Integrator, but limited with Researcher
    ("Critic", "Writer"): 1.0,
    ("Critic", "Researcher"): 0.3,
    ("Critic", "Integrator"): 1.0,
    
    # Integrator can communicate with everyone (coordination role)
    ("Integrator", "Researcher"): 1.0,
    ("Integrator", "Writer"): 1.0,
    ("Integrator", "Critic"): 1.0,
}

# Default value for pairs not explicitly in the matrix
DEFAULT_COMMUNICATION_PERMISSION = 0.0

# Function to check if communication is allowed between two agents
def is_communication_allowed(sender_name, recipient_name):
    """Check if communication is allowed between sender and recipient"""
    permission = COMMUNICATION_MATRIX.get(
        (sender_name, recipient_name), 
        DEFAULT_COMMUNICATION_PERMISSION
    )
    return permission >= 0.5  # Allow if permission value is 0.5 or higher

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

# A custom middleware wrapping function to enforce communication rules
async def communication_middleware_activity(activity_fn, *args, **kwargs):
    """Middleware to check if communication is allowed before executing a messaging activity"""
    # Extract sender and recipient from args (specific to our messaging activities)
    if len(args) >= 2:  # Make sure we have sender and recipient
        sender = args[0]
        recipient = args[1]
        
        # Extract names (handle different formats)
        sender_name = sender["name"] if isinstance(sender, dict) else sender.name
        
        # Handle single recipient or list of recipients
        if isinstance(recipient, list):
            # For lists, check each recipient
            allowed_recipients = []
            for r in recipient:
                r_name = r["name"] if isinstance(r, dict) else r.name
                if is_communication_allowed(sender_name, r_name):
                    allowed_recipients.append(r)
                else:
                    print(f"⛔ Communication blocked: {sender_name} -> {r_name} (not allowed)")
            
            if not allowed_recipients:
                print(f"⛔ All communications blocked for {sender_name}. No allowed recipients.")
                return {"error": "Communication not allowed", "blocked": True}
            
            # Replace with filtered list
            args_list = list(args)
            args_list[1] = allowed_recipients
            args = tuple(args_list)
        else:
            # Single recipient
            recipient_name = recipient["name"] if isinstance(recipient, dict) else recipient.name
            if not is_communication_allowed(sender_name, recipient_name):
                print(f"⛔ Communication blocked: {sender_name} -> {recipient_name} (not allowed)")
                return {"error": "Communication not allowed", "blocked": True}
    
    # If we get here, communication is allowed (or this isn't a messaging activity)
    return await activity_fn(*args, **kwargs)

# Override messaging functions to use middleware
original_send_message = send_message
original_ask_question = ask_question
original_provide_answer = provide_answer
original_make_proposal = make_proposal
original_provide_feedback = provide_feedback

# Replace with middleware-wrapped versions
send_message = lambda *args, **kwargs: communication_middleware_activity(original_send_message, *args, **kwargs)
ask_question = lambda *args, **kwargs: communication_middleware_activity(original_ask_question, *args, **kwargs)
provide_answer = lambda *args, **kwargs: communication_middleware_activity(original_provide_answer, *args, **kwargs)
make_proposal = lambda *args, **kwargs: communication_middleware_activity(original_make_proposal, *args, **kwargs)
provide_feedback = lambda *args, **kwargs: communication_middleware_activity(original_provide_feedback, *args, **kwargs)

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
    print(f"\n{'-'*20} AGENT COMMUNICATION PERMISSIONS {'-'*20}")
    print("The following agent communication paths are enabled:")
    for (sender, recipient), permission in sorted(COMMUNICATION_MATRIX.items()):
        status = "✅ ALLOWED" if permission >= 0.5 else "❌ BLOCKED"
        print(f"  {sender} -> {recipient}: {permission:.1f} ({status})")
    print(f"{'-'*65}\n")
    
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
            
            # Communication activities - using original versions (middleware handled separately)
            original_send_message,
            original_ask_question,
            original_provide_answer,
            original_make_proposal,
            original_provide_feedback,
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