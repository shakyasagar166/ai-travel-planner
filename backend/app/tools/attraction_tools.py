from typing import List, Dict, Any, Optional
from langchain_core.tools import tool
from app.database.session import SessionLocal, get_engine
from app.database.models import Attraction, Destination


@tool
def search_attractions(destination_name: str, category: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Search for attractions and sightseeing spots in a destination, optionally filtered by category (Adventure, Heritage, Nature, Food, Culture).
    """
    if SessionLocal is None:
        get_engine()
    db = SessionLocal()
    try:
        dest = db.query(Destination).filter(
            (Destination.name.ilike(f"%{destination_name}%")) |
            (Destination.city.ilike(f"%{destination_name}%"))
        ).first()

        if not dest:
            return []

        q = db.query(Attraction).filter(Attraction.destination_id == dest.id)
        if category:
            q = q.filter(Attraction.category.ilike(f"%{category}%"))

        attractions = q.all()
        return [
            {
                "id": a.id,
                "name": a.name,
                "category": a.category,
                "description": a.description,
                "duration_hours": a.duration_hours,
                "entry_fee_inr": a.entry_fee_inr,
                "rating": a.rating,
                "best_time_of_day": a.best_time_of_day
            }
            for a in attractions
        ]
    finally:
        db.close()


@tool
def filter_attractions_by_interests(destination_id: int, interests: List[str]) -> List[Dict[str, Any]]:
    """
    Filter and rank attractions in a destination matching user's specific interest list.
    """
    if SessionLocal is None:
        get_engine()
    db = SessionLocal()
    try:
        attractions = db.query(Attraction).filter(Attraction.destination_id == destination_id).all()
        scored = []
        interests_lower = [i.lower() for i in interests]

        for a in attractions:
            score = 0
            cat_lower = a.category.lower()
            desc_lower = a.description.lower()
            for interest in interests_lower:
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
                "relevance_score": score
            })

        scored.sort(key=lambda x: (x["relevance_score"], x["rating"]), reverse=True)
        return scored
    finally:
        db.close()
