from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.database.models import User, UserPreference
from app.database.schemas import UserRegister, UserPreferenceUpdate
from app.core.security import get_password_hash, verify_password


class AuthService:
    @staticmethod
    def register(db: Session, data: UserRegister) -> User:
        existing = db.query(User).filter(User.email == data.email.lower()).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email is already registered"
            )

        user = User(
            email=data.email.lower(),
            hashed_password=get_password_hash(data.password),
            full_name=data.full_name,
            is_active=True
        )
        db.add(user)
        db.flush()

        pref = UserPreference(
            user_id=user.id,
            preferred_travel_style="Balanced",
            budget_tier="Moderate",
            dietary_preferences="Any",
            pace_preference="Moderate",
            interests_json=[]
        )
        db.add(pref)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def authenticate(db: Session, email: str, password: str) -> User:
        user = db.query(User).filter(User.email == email.lower()).first()
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User account is deactivated"
            )
        return user

    @staticmethod
    def get_preferences(db: Session, user_id: int) -> UserPreference:
        pref = db.query(UserPreference).filter(UserPreference.user_id == user_id).first()
        if not pref:
            pref = UserPreference(user_id=user_id)
            db.add(pref)
            db.commit()
            db.refresh(pref)
        return pref

    @staticmethod
    def update_preferences(db: Session, user_id: int, data: UserPreferenceUpdate) -> UserPreference:
        pref = AuthService.get_preferences(db, user_id)
        if data.preferred_travel_style is not None:
            pref.preferred_travel_style = data.preferred_travel_style
        if data.budget_tier is not None:
            pref.budget_tier = data.budget_tier
        if data.dietary_preferences is not None:
            pref.dietary_preferences = data.dietary_preferences
        if data.pace_preference is not None:
            pref.pace_preference = data.pace_preference
        if data.interests is not None:
            pref.interests_json = data.interests

        db.commit()
        db.refresh(pref)
        return pref
