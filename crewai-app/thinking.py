from dataclasses import dataclass
from typing import List, Optional, Dict, Any
import time
from temporalio import activity
import asyncio

# Define detailed thinking structure
@dataclass
class ThinkingStep:
    content: str
    step_number: int
    reasoning: str  # Why this thought is relevant
    evidence: List[str] = None  # Supporting evidence for this thought
    conclusion: Optional[str] = None  # What was concluded from this thought

# Define thinking activities
@activity.defn
async def researcher_detailed_thinking(agent: Any, thinking: ThinkingStep) -> Dict[str, Any]:
    """Capture a researcher's detailed thinking process"""
    timestamp = time.strftime("%H:%M:%S")
    
    # Handle both AgentConfig objects and dictionaries
    agent_name = agent["name"] if isinstance(agent, dict) else agent.name
    
    # Format the thinking step in a clear way
    print(f"\n[{timestamp}] 🧠 {agent_name} THINKING (Step {thinking.step_number}):")
    print(f"  THOUGHT: {thinking.content}")
    print(f"  REASONING: {thinking.reasoning}")
    
    if thinking.evidence:
        print("  EVIDENCE:")
        for i, point in enumerate(thinking.evidence):
            print(f"    {i+1}. {point}")
    
    if thinking.conclusion:
        print(f"  CONCLUSION: {thinking.conclusion}")
    
    # Return the complete thinking step as a dict for logging
    return {
        "agent": agent_name,
        "timestamp": timestamp,
        "step": thinking.step_number,
        "thought": thinking.content,
        "reasoning": thinking.reasoning,
        "evidence": thinking.evidence,
        "conclusion": thinking.conclusion
    }

@activity.defn
async def writer_detailed_thinking(agent: Any, thinking: ThinkingStep) -> Dict[str, Any]:
    """Capture a writer's detailed thinking process"""
    timestamp = time.strftime("%H:%M:%S")
    
    # Handle both AgentConfig objects and dictionaries
    agent_name = agent["name"] if isinstance(agent, dict) else agent.name
    
    # Format the thinking step in a clear way
    print(f"\n[{timestamp}] 🧠 {agent_name} THINKING (Step {thinking.step_number}):")
    print(f"  THOUGHT: {thinking.content}")
    print(f"  REASONING: {thinking.reasoning}")
    
    if thinking.evidence:
        print("  EVIDENCE:")
        for i, point in enumerate(thinking.evidence):
            print(f"    {i+1}. {point}")
    
    if thinking.conclusion:
        print(f"  CONCLUSION: {thinking.conclusion}")
    
    # Return the complete thinking step as a dict for logging
    return {
        "agent": agent_name,
        "timestamp": timestamp,
        "step": thinking.step_number,
        "thought": thinking.content,
        "reasoning": thinking.reasoning,
        "evidence": thinking.evidence,
        "conclusion": thinking.conclusion
    }

@activity.defn
async def researcher_think(agent: Any, thought: str) -> str:
    """Capture a researcher's thinking process"""
    timestamp = time.strftime("%H:%M:%S")
    # Handle both AgentConfig objects and dictionaries
    agent_name = agent["name"] if isinstance(agent, dict) else agent.name
    print(f"[{timestamp}] 🧠 {agent_name} is thinking: {thought}")
    return f"Thought recorded: {thought}"

@activity.defn
async def writer_think(agent: Any, thought: str) -> str:
    """Capture a writer's thinking process"""
    timestamp = time.strftime("%H:%M:%S")
    # Handle both AgentConfig objects and dictionaries
    agent_name = agent["name"] if isinstance(agent, dict) else agent.name
    print(f"[{timestamp}] 🧠 {agent_name} is thinking: {thought}")
    return f"Thought recorded: {thought}" 