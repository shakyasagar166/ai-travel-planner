import logging
from typing import Dict, Any, List
from app.agents.state import TravelState
from app.database.session import SessionLocal, get_engine
from app.database.models import Attraction

logger = logging.getLogger(__name__)


def attraction_agent(state: TravelState) -> Dict[str, Any]:
    """
    Selects and ranks attractions based on duration, traveler interests, and ratings.
    """
    matched_dest = state.get("matched_destination")
    interests = [i.lower() for i in state.get("interests", [])]
    days = state.get("days", 3)

    if not matched_dest:
        return {"selected_attractions": []}

    dest_id = matched_dest["id"]

    if SessionLocal is None:
        get_engine()
    db = SessionLocal()

    selected = []
    try:
        attractions = db.query(Attraction).filter(Attraction.destination_id == dest_id).all()
        scored = []
        for a in attractions:
            score = 0
            cat_lower = a.category.lower()
            desc_lower = a.description.lower()
            for interest in interests:
                if interest in cat_lower:
                    score += 3
                if interest in desc_lower:
                    score += 1

            scored.append({
                "id": a.id,
                "name": a.name,
                "category": a.category,
                "description": a.description,
                "duration_hours": a.duration_hours,
                "entry_fee_inr": a.entry_fee_inr,
                "rating": a.rating,
                "best_time_of_day": a.best_time_of_day,
                "image_url": a.image_url,
                "score": score
            })

        # Sort primarily by relevance, then rating
        scored.sort(key=lambda x: (x["score"], x["rating"]), reverse=True)
        # Select enough attractions for the trip (e.g. 2 to 3 per day)
        needed = min(len(scored), days * 3)
        selected = scored[:needed]
    finally:
        db.close()

    steps = state.get("agent_steps", [])
    steps.append({
        "agent": "attraction_curation",
        "status": "completed",
        "output": f"Curated {len(selected)} top-rated attractions matching interests ({', '.join(interests) if interests else 'General'})"
    })

    return {
        "selected_attractions": selected,
        "agent_steps": steps
    }
