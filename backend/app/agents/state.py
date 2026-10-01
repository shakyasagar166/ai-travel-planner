from typing import TypedDict, List, Dict, Any, Optional


class TravelState(TypedDict, total=False):
    """
    Central state shared across all agents in the LangGraph travel planning workflow.
    """
    # User Input
    user_query: str
    user_id: Optional[int]

    # Extracted Requirements
    destination: Optional[str]
    days: int
    budget: float
    travelers_count: int
    travel_style: str  # Adventure, Cultural, Relaxed, Foodie, Balanced
    interests: List[str]
    diet: str
    pace: str
    extracted_requirements: Dict[str, Any]

    # Agent Processing Data
    matched_destination: Optional[Dict[str, Any]]
    selected_attractions: List[Dict[str, Any]]
    selected_accommodation: Optional[Dict[str, Any]]
    day_by_day_plan: List[Dict[str, Any]]
    cost_breakdown: Optional[Dict[str, Any]]
    rag_context: str
    insider_tips: List[str]
    packing_checklist: List[str]

    # Output & Diagnostics
    agent_steps: List[Dict[str, str]]
    final_response: str
    itinerary_payload: Optional[Dict[str, Any]]
