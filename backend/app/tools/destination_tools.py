from typing import List, Dict, Any, Optional
from langchain_core.tools import tool
from app.database.session import SessionLocal, get_engine
from app.database.models import Destination


@tool
def search_destinations(query: str, continent: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Search available destinations by city, country, or keyword tags (e.g. beach, mountains, heritage).
    """
    if SessionLocal is None:
        get_engine()
    db = SessionLocal()
    try:
        q = db.query(Destination)
        if continent:
            q = q.filter(Destination.continent.ilike(f"%{continent}%"))

        q = q.filter(
            (Destination.name.ilike(f"%{query}%")) |
            (Destination.country.ilike(f"%{query}%")) |
            (Destination.city.ilike(f"%{query}%")) |
            (Destination.description.ilike(f"%{query}%"))
        )
        destinations = q.all()
        return [
            {
                "id": d.id,
                "name": d.name,
                "city": d.city,
                "country": d.country,
                "best_season": d.best_season,
                "avg_daily_budget_inr": d.avg_daily_budget_inr,
                "tags": d.tags_json or []
            }
            for d in destinations
        ]
    finally:
        db.close()


@tool
def get_destination_details(destination_id: int) -> Dict[str, Any]:
    """
    Retrieves complete details for a specific destination by its ID.
    """
    if SessionLocal is None:
        get_engine()
    db = SessionLocal()
    try:
        dest = db.query(Destination).filter(Destination.id == destination_id).first()
        if not dest:
            return {"error": f"Destination with id {destination_id} not found"}
        return {
            "id": dest.id,
            "name": dest.name,
            "city": dest.city,
            "country": dest.country,
            "climate": dest.climate,
            "best_season": dest.best_season,
            "currency": dest.currency,
            "avg_daily_budget_inr": dest.avg_daily_budget_inr,
            "description": dest.description,
            "attractions_count": len(dest.attractions),
            "accommodations_count": len(dest.accommodations)
        }
    finally:
        db.close()
