from dataclasses import dataclass
from temporalio import activity
from typing import Dict, Any, List, Optional

# Agent configuration class
@dataclass
class AgentConfig:
    name: str
    role: str
    goal: str
    backstory: str
    skills: List[str] = None
    knowledge_areas: List[str] = None
    communication_style: Optional[str] = None

# Agent setup activities
@activity.defn
async def setup_researcher_agent() -> AgentConfig:
    """Create and initialize the researcher agent"""
    print("Setting up researcher agent")
    
    # Here you would initialize a CrewAI agent
    researcher = AgentConfig(
        name="Researcher",
        role="Research Expert",
        goal="Research the latest AI technologies",
        backstory="You are an AI research expert with deep knowledge of modern AI systems",
        skills=["Data Analysis", "Literature Review", "Technical Research"],
        knowledge_areas=["AI Systems", "Machine Learning", "Temporal Architecture"],
        communication_style="Analytical and detail-oriented"
    )
    
    print(f"Created agent: {researcher.name}")
    return researcher

@activity.defn
async def setup_writer_agent() -> AgentConfig:
    """Create and initialize the writer agent"""
    print("Setting up writer agent")
    
    # Here you would initialize a CrewAI agent
    writer = AgentConfig(
        name="Writer",
        role="Technical Writer",
        goal="Communicate complex AI concepts clearly",
        backstory="You specialize in technical writing with a focus on making complex topics accessible",
        skills=["Content Creation", "Editing", "Simplifying Technical Concepts"],
        knowledge_areas=["Technical Documentation", "AI Applications", "Communication Best Practices"],
        communication_style="Clear and educational"
    )
    
    print(f"Created agent: {writer.name}")
    return writer

@activity.defn
async def setup_critic_agent() -> AgentConfig:
    """Create and initialize a critic agent to provide feedback"""
    print("Setting up critic agent")
    
    critic = AgentConfig(
        name="Critic",
        role="Quality Assurance Specialist",
        goal="Ensure accuracy and completeness of information",
        backstory="You are a detail-oriented reviewer who evaluates content for technical accuracy and clarity",
        skills=["Critical Analysis", "Quality Assurance", "Technical Validation"],
        knowledge_areas=["AI Systems", "Technical Documentation Standards", "Common Implementation Pitfalls"],
        communication_style="Direct and constructive"
    )
    
    print(f"Created agent: {critic.name}")
    return critic

@activity.defn
async def setup_integrator_agent() -> AgentConfig:
    """Create and initialize an integrator agent that helps coordinate between other agents"""
    print("Setting up integrator agent")
    
    integrator = AgentConfig(
        name="Integrator",
        role="Project Coordinator",
        goal="Facilitate collaboration and integrate contributions from different agents",
        backstory="You excel at coordinating complex projects and helping diverse specialists work together effectively",
        skills=["Project Management", "Conflict Resolution", "Decision Making", "Synthesis"],
        knowledge_areas=["Team Dynamics", "AI Project Management", "Systems Integration"],
        communication_style="Diplomatic and inclusive"
    )
    
    print(f"Created agent: {integrator.name}")
    return integrator

@activity.defn
async def agent_response_to_feedback(agent: Any, feedback: str, topic: str) -> Dict[str, Any]:
    """Generate a response to feedback for the agent"""
    agent_name = agent["name"] if isinstance(agent, dict) else agent.name
    agent_role = agent["role"] if isinstance(agent, dict) else agent.role
    
    print(f"Agent {agent_name} responding to feedback on {topic}")
    
    # In real implementation, we would use the agent's actual reasoning
    response = {
        "agent": agent_name,
        "original_feedback": feedback,
        "response": f"Thank you for the feedback. As a {agent_role}, I will incorporate these suggestions to improve the {topic}.",
        "changes_planned": [
            "Add more specific examples",
            "Clarify technical terminology",
            "Address the concerns about implementation steps"
        ],
        "additional_questions": [
            "Could you specify which aspects need more detailed examples?",
            "Are there particular terms that require better explanation?"
        ]
    }
    
    print(f"Agent {agent_name} has formulated a response to feedback")
    return response

@activity.defn
async def resolve_agent_disagreement(agents: List[Any], topic: str, positions: List[str]) -> Dict[str, Any]:
    """Resolve a disagreement between agents"""
    agent_names = [agent["name"] if isinstance(agent, dict) else agent.name for agent in agents]
    
    print(f"Resolving disagreement between {', '.join(agent_names)} on {topic}")
    
    # In real implementation, would involve complex negotiation between agents
    resolution = {
        "topic": topic,
        "agents_involved": agent_names,
        "original_positions": positions,
        "resolution_process": [
            "Identified core points of disagreement",
            "Found common ground on key aspects",
            "Negotiated compromise on contentious issues",
            "Synthesized a solution incorporating multiple perspectives"
        ],
        "final_resolution": f"The agents have agreed on a compromise approach to {topic} that incorporates elements from each perspective.",
        "consensus_level": "Medium-high"
    }
    
    print(f"Disagreement resolved with {resolution['consensus_level']} consensus")
    return resolution 