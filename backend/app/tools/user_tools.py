from typing import Dict, Any
from langchain_core.tools import tool
from app.database.session import SessionLocal, get_engine
from app.database.models import UserPreference


@tool
def get_user_travel_preferences(user_id: int) -> Dict[str, Any]:
    """
    Retrieves stored travel preferences (budget tier, travel style, dietary habits, interests) for a user.
    """
    if SessionLocal is None:
        get_engine()
    db = SessionLocal()
    try:
        pref = db.query(UserPreference).filter(UserPreference.user_id == user_id).first()
        if not pref:
            return {
                "preferred_travel_style": "Balanced",
                "budget_tier": "Moderate",
                "dietary_preferences": "Any",
                "pace_preference": "Moderate",
                "interests": []
            }
        return {
            "preferred_travel_style": pref.preferred_travel_style,
            "budget_tier": pref.budget_tier,
            "dietary_preferences": pref.dietary_preferences,
            "pace_preference": pref.pace_preference,
            "interests": pref.interests_json or []
        }
    finally:
        db.close()


@tool
def save_user_travel_preference(user_id: int, key: str, value: Any) -> Dict[str, Any]:
    """
    Updates a specific travel preference field for a user.
    """
    if SessionLocal is None:
        get_engine()
    db = SessionLocal()
    try:
        pref = db.query(UserPreference).filter(UserPreference.user_id == user_id).first()
        if not pref:
            pref = UserPreference(user_id=user_id)
            db.add(pref)

        if key == "preferred_travel_style":
            pref.preferred_travel_style = str(value)
        elif key == "budget_tier":
            pref.budget_tier = str(value)
        elif key == "dietary_preferences":
            pref.dietary_preferences = str(value)
        elif key == "pace_preference":
            pref.pace_preference = str(value)

        db.commit()
        return {"status": "success", "updated_field": key, "new_value": value}
    finally:
        db.close()
