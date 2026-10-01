import logging
from typing import Dict, Any
from app.agents.state import TravelState
from app.database.session import SessionLocal, get_engine
from app.database.models import Accommodation

logger = logging.getLogger(__name__)


def accommodation_agent(state: TravelState) -> Dict[str, Any]:
    """
    Selects the optimal accommodation (Hostel, Hotel, Resort) matching traveler's budget and tier.
    """
    matched_dest = state.get("matched_destination")
    budget = state.get("budget", 0)
    days = state.get("days", 3)
    travel_style = state.get("travel_style", "Balanced").lower()

    if not matched_dest:
        return {"selected_accommodation": None}

    dest_id = matched_dest["id"]

    # Determine desired tier based on budget or style
    if "luxury" in travel_style or (budget > 0 and budget / max(1, days) > 15000):
        target_tier = "Luxury"
    elif "budget" in travel_style or "hostel" in travel_style or (budget > 0 and budget / max(1, days) < 3000):
        target_tier = "Budget"
    else:
        target_tier = "Moderate"

    if SessionLocal is None:
        get_engine()
    db = SessionLocal()

    selected = None
    try:
        # Search by target tier
        hotel = db.query(Accommodation).filter(
            Accommodation.destination_id == dest_id,
            Accommodation.tier.ilike(f"%{target_tier}%")
        ).order_by(Accommodation.rating.desc()).first()

        if not hotel:
            hotel = db.query(Accommodation).filter(
                Accommodation.destination_id == dest_id
            ).order_by(Accommodation.rating.desc()).first()

        if hotel:
            selected = {
                "id": hotel.id,
                "name": hotel.name,
                "tier": hotel.tier,
                "price_per_night_inr": hotel.price_per_night_inr,
                "rating": hotel.rating,
                "address": hotel.address,
                "amenities": hotel.amenities_json or [],
                "image_url": hotel.image_url
            }
    finally:
        db.close()

    steps = state.get("agent_steps", [])
    hotel_name = selected["name"] if selected else "Standard Hotel"
    hotel_price = selected["price_per_night_inr"] if selected else 2500
    steps.append({
        "agent": "accommodation_matcher",
        "status": "completed",
        "output": f"Selected stay: {hotel_name} ({selected.get('tier') if selected else 'Moderate'}) @ ₹{hotel_price:,.0f}/night"
    })

    return {
        "selected_accommodation": selected,
        "agent_steps": steps
    }
