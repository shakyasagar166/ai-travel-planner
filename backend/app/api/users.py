from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.database.models import User
from app.database.schemas import UserPreferenceUpdate, UserPreferenceResponse
from app.services.auth_service import AuthService
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/users", tags=["Users & Preferences"])


@router.get("/preferences", response_model=UserPreferenceResponse)
def get_preferences(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieve traveler preferences for authenticated user."""
    return AuthService.get_preferences(db, current_user.id)


@router.put("/preferences", response_model=UserPreferenceResponse)
def update_preferences(
    pref_in: UserPreferenceUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update traveler preferences for authenticated user."""
    return AuthService.update_preferences(db, current_user.id, pref_in)
