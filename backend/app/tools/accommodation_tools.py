from typing import List, Dict, Any, Optional
from langchain_core.tools import tool
from app.database.session import SessionLocal, get_engine
from app.database.models import Accommodation, Destination


@tool
def search_accommodations(
    destination_name: str,
    tier: Optional[str] = None,
    max_price_per_night: Optional[float] = None
) -> List[Dict[str, Any]]:
    """
    Search hotels, hostels, and resorts in a destination by tier (Budget, Moderate, Luxury) or max price.
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

        q = db.query(Accommodation).filter(Accommodation.destination_id == dest.id)
        if tier:
            q = q.filter(Accommodation.tier.ilike(f"%{tier}%"))
        if max_price_per_night:
            q = q.filter(Accommodation.price_per_night_inr <= max_price_per_night)

        hotels = q.order_by(Accommodation.rating.desc()).all()
        return [
            {
                "id": h.id,
                "name": h.name,
                "tier": h.tier,
                "price_per_night_inr": h.price_per_night_inr,
                "rating": h.rating,
                "address": h.address,
                "amenities": h.amenities_json or []
            }
            for h in hotels
        ]
    finally:
        db.close()
