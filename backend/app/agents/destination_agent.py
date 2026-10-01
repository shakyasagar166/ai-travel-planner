import logging
from typing import Dict, Any
from app.agents.state import TravelState
from app.database.session import SessionLocal, get_engine
from app.database.models import Destination

logger = logging.getLogger(__name__)


def destination_agent(state: TravelState) -> Dict[str, Any]:
    """
    Finds and resolves the best matching destination from the catalog.
    """
    dest_name = state.get("destination")
    interests = state.get("interests", [])

    if SessionLocal is None:
        get_engine()
    db = SessionLocal()

    matched = None
    try:
        if dest_name:
            dest = db.query(Destination).filter(
                (Destination.name.ilike(f"%{dest_name}%")) |
                (Destination.city.ilike(f"%{dest_name}%"))
            ).first()
            if dest:
                matched = {
                    "id": dest.id,
                    "name": dest.name,
                    "city": dest.city,
                    "country": dest.country,
                    "continent": dest.continent,
                    "climate": dest.climate,
                    "best_season": dest.best_season,
                    "currency": dest.currency,
                    "avg_daily_budget_inr": dest.avg_daily_budget_inr,
                    "description": dest.description,
                    "image_url": dest.image_url,
                    "tags": dest.tags_json or []
                }

        # If not found by name, search by tags
        if not matched:
            all_dest = db.query(Destination).all()
            for d in all_dest:
                tags = [t.lower() for t in (d.tags_json or [])]
                if any(i.lower() in tags for i in interests):
                    matched = {
                        "id": d.id,
                        "name": d.name,
                        "city": d.city,
                        "country": d.country,
                        "continent": d.continent,
                        "climate": d.climate,
                        "best_season": d.best_season,
                        "currency": d.currency,
                        "avg_daily_budget_inr": d.avg_daily_budget_inr,
                        "description": d.description,
                        "image_url": d.image_url,
                        "tags": d.tags_json or []
                    }
                    break

            if not matched and all_dest:
                d = all_dest[0]
                matched = {
                    "id": d.id,
                    "name": d.name,
                    "city": d.city,
                    "country": d.country,
                    "continent": d.continent,
                    "climate": d.climate,
                    "best_season": d.best_season,
                    "currency": d.currency,
                    "avg_daily_budget_inr": d.avg_daily_budget_inr,
                    "description": d.description,
                    "image_url": d.image_url,
                    "tags": d.tags_json or []
                }
    finally:
        db.close()

    steps = state.get("agent_steps", [])
    dest_title = matched["name"] if matched else "Default"
    steps.append({
        "agent": "destination_selection",
        "status": "completed",
        "output": f"Selected destination: {dest_title} ({matched.get('country') if matched else ''}) with best season: {matched.get('best_season') if matched else ''}"
    })

    return {
        "matched_destination": matched,
        "destination": matched["name"] if matched else dest_name,
        "agent_steps": steps
    }
