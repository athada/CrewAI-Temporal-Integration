from dataclasses import dataclass
from temporalio import activity

# Agent configuration class
@dataclass
class AgentConfig:
    name: str
    role: str
    goal: str
    backstory: str

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
        backstory="You are an AI research expert with deep knowledge of modern AI systems"
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
        backstory="You specialize in technical writing with a focus on making complex topics accessible"
    )
    
    print(f"Created agent: {writer.name}")
    return writer 