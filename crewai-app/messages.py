from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import time
from temporalio import activity
import uuid
import json
import os

@dataclass
class Message:
    sender: str
    recipient: str
    content: str
    message_type: str  # 'question', 'answer', 'proposal', 'feedback', etc.
    message_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: float = field(default_factory=time.time)
    related_to: Optional[str] = None  # ID of message this is responding to
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Conversation:
    conversation_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    messages: List[Message] = field(default_factory=list)
    topic: Optional[str] = None
    status: str = "active"  # active, completed, etc.
    timestamp: float = field(default_factory=time.time)

# Global store for conversations
CONVERSATION_STORE = {}
MESSAGE_LOG_DIR = "/tmp/agent_messages"

# Do NOT create directories here, as it will be executed inside workflow sandbox
# Instead, we'll create the directory during activity execution

# Message handling activities
@activity.defn
async def send_message(sender: Dict[str, Any], recipient: Any, 
                      content: str, message_type: str, 
                      conversation_id: Optional[str] = None,
                      related_to: Optional[str] = None) -> Dict[str, Any]:
    """Send a message from one agent to another or to multiple agents"""
    sender_name = sender["name"] if isinstance(sender, dict) else sender.name
    
    # Handle individual recipient or list of recipients
    if isinstance(recipient, list):
        # For multiple recipients, get all names
        recipient_names = []
        for r in recipient:
            if isinstance(r, dict):
                recipient_names.append(r["name"])
            else:
                recipient_names.append(r.name)
        recipient_name = ", ".join(recipient_names)
    else:
        # Single recipient
        recipient_name = recipient["name"] if isinstance(recipient, dict) else recipient.name
    
    # Create the message
    message = Message(
        sender=sender_name,
        recipient=recipient_name,
        content=content,
        message_type=message_type,
        related_to=related_to
    )
    
    # Create or retrieve conversation
    if conversation_id is None or conversation_id not in CONVERSATION_STORE:
        conversation = Conversation(topic=f"Conversation between {sender_name} and {recipient_name}")
        CONVERSATION_STORE[conversation.conversation_id] = conversation
        conversation_id = conversation.conversation_id
    else:
        conversation = CONVERSATION_STORE[conversation_id]
    
    # Add message to conversation
    conversation.messages.append(message)
    
    # Log the message
    timestamp = time.strftime("%H:%M:%S")
    print(f"\n[{timestamp}] 💬 Message from {sender_name} to {recipient_name}:")
    print(f"  Type: {message_type}")
    print(f"  Content: {content}")
    
    # Create directory and save message to file - safe in an activity
    try:
        os.makedirs(MESSAGE_LOG_DIR, exist_ok=True)
        log_file = f"{MESSAGE_LOG_DIR}/conversation_{conversation_id}.json"
        with open(log_file, "w") as f:
            json.dump({
                "conversation_id": conversation_id,
                "topic": conversation.topic,
                "messages": [vars(msg) for msg in conversation.messages]
            }, f, indent=2, default=str)
    except Exception as e:
        print(f"Warning: Could not save message log: {e}")
    
    # Return message info
    return {
        "message_id": message.message_id,
        "conversation_id": conversation_id,
        "sender": sender_name,
        "recipient": recipient_name,
        "content": content,
        "timestamp": message.timestamp
    }

@activity.defn
async def ask_question(sender: Dict[str, Any], recipient: Dict[str, Any], 
                      question: str, conversation_id: Optional[str] = None) -> Dict[str, Any]:
    """Ask a question to another agent"""
    return await send_message(
        sender=sender,
        recipient=recipient,
        content=question,
        message_type="question",
        conversation_id=conversation_id
    )

@activity.defn
async def provide_answer(sender: Dict[str, Any], recipient: Dict[str, Any], 
                        answer: str, question_message_id: str,
                        conversation_id: str) -> Dict[str, Any]:
    """Answer a question from another agent"""
    return await send_message(
        sender=sender,
        recipient=recipient,
        content=answer,
        message_type="answer",
        conversation_id=conversation_id,
        related_to=question_message_id
    )

@activity.defn
async def make_proposal(sender: Dict[str, Any], recipient: Any, 
                       proposal: str, conversation_id: Optional[str] = None) -> Dict[str, Any]:
    """Make a proposal to another agent or to multiple agents"""
    return await send_message(
        sender=sender,
        recipient=recipient,
        content=proposal,
        message_type="proposal",
        conversation_id=conversation_id
    )

@activity.defn
async def provide_feedback(sender: Dict[str, Any], recipient: Dict[str, Any], 
                          feedback: str, proposal_message_id: str,
                          conversation_id: str) -> Dict[str, Any]:
    """Provide feedback on a proposal"""
    return await send_message(
        sender=sender,
        recipient=recipient,
        content=feedback,
        message_type="feedback",
        conversation_id=conversation_id,
        related_to=proposal_message_id
    )

@activity.defn
async def get_conversation_history(conversation_id: str) -> List[Dict[str, Any]]:
    """Retrieve the conversation history"""
    if conversation_id not in CONVERSATION_STORE:
        return []
    
    conversation = CONVERSATION_STORE[conversation_id]
    return [vars(msg) for msg in conversation.messages]

@activity.defn
async def collaborate_on_decision(agents: List[Dict[str, Any]], topic: str, 
                                 initial_proposal: str) -> Dict[str, Any]:
    """Orchestrate a collaborative decision-making process between agents"""
    if len(agents) < 2:
        raise ValueError("Collaboration requires at least two agents")
    
    # Create a new conversation for this collaboration
    conversation = Conversation(topic=f"Collaboration on: {topic}")
    CONVERSATION_STORE[conversation.conversation_id] = conversation
    
    # Get agent names
    agent_names = [agent["name"] if isinstance(agent, dict) else agent.name for agent in agents]
    
    # Log the start of collaboration
    timestamp = time.strftime("%H:%M:%S")
    print(f"\n[{timestamp}] 🤝 Starting collaboration between {', '.join(agent_names)}")
    print(f"  Topic: {topic}")
    print(f"  Initial proposal: {initial_proposal}")
    
    # Simulated collaborative decision-making
    # In a real implementation, this would involve back-and-forth communication
    result = {
        "collaboration_id": conversation.conversation_id,
        "topic": topic,
        "participants": agent_names,
        "final_decision": f"Agreed to proceed with: {initial_proposal} with some modifications",
        "consensus_level": "high",
        "timestamp": time.time()
    }
    
    # Log the result
    print(f"\n[{timestamp}] ✅ Collaboration complete")
    print(f"  Decision: {result['final_decision']}")
    print(f"  Consensus level: {result['consensus_level']}")
    
    return result 