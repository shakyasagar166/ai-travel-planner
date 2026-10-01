import logging
from typing import Dict, Any
from app.agents.state import TravelState

logger = logging.getLogger(__name__)


def supervisor_agent(state: TravelState) -> Dict[str, Any]:
    """
    Supervisor / Planner agent coordinating workflow transitions and verifying state.
    """
    steps = state.get("agent_steps", [])
    steps.append({
        "agent": "supervisor_planner",
        "status": "completed",
        "output": "Orchestrating multi-agent execution pipeline: Destination -> Attractions -> Stays -> Schedule -> Budget -> RAG -> Final"
    })
    return {"agent_steps": steps}
