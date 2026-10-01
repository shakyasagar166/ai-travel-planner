import uuid
import logging
from typing import Optional
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.database.models import User, Conversation, Message
from app.database.schemas import ChatRequest, ChatResponse, AgentStep
from app.core.dependencies import get_optional_current_user
from app.graph.travel_graph import travel_app

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/chat", tags=["AI Travel Agent Chat"])


@router.post("", response_model=ChatResponse)
def chat_with_agent(
    req: ChatRequest,
    current_user: Optional[User] = Depends(get_optional_current_user),
    db: Session = Depends(get_db)
):
    """
    Executes the LangGraph autonomous multi-agent travel planning workflow.
    """
    conv_id = req.conversation_id or str(uuid.uuid4())

    # Get or create conversation record
    conv = db.query(Conversation).filter(Conversation.id == conv_id).first()
    if not conv:
        conv = Conversation(
            id=conv_id,
            user_id=current_user.id if current_user else None,
            title=req.message[:50] + "..." if len(req.message) > 50 else req.message
        )
        db.add(conv)
        db.commit()

    # Save user message
    user_msg = Message(
        conversation_id=conv_id,
        sender="user",
        content=req.message
    )
    db.add(user_msg)
    db.commit()

    # Prepare LangGraph State
    initial_state = {
        "user_query": req.message,
        "user_id": current_user.id if current_user else None,
        "agent_steps": []
    }

    logger.info(f"Invoking LangGraph Travel Workflow for query: '{req.message}'...")
    final_state = travel_app.invoke(initial_state)

    final_text = final_state.get("final_response", "Unable to generate travel plan.")
    itinerary_data = final_state.get("itinerary_payload")
    agent_steps = final_state.get("agent_steps", [])

    # Save assistant message
    asst_msg = Message(
        conversation_id=conv_id,
        sender="assistant",
        content=final_text,
        agent_steps_json=agent_steps,
        itinerary_json=itinerary_data
    )
    db.add(asst_msg)
    db.commit()

    return {
        "conversation_id": conv_id,
        "response": final_text,
        "itinerary": itinerary_data,
        "agent_steps": [
            AgentStep(agent=s.get("agent", ""), status=s.get("status", "completed"), output=s.get("output", ""))
            for s in agent_steps
        ]
    }
