from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.database.models import Trip, User
from app.database.schemas import TripCreate, TripResponse
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/trips", tags=["Trips & Saved Itineraries"])


@router.post("", response_model=TripResponse, status_code=status.HTTP_201_CREATED)
def save_trip(
    trip_in: TripCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Saves a customized itinerary for the authenticated user."""
    trip = Trip(
        user_id=current_user.id,
        title=trip_in.title,
        destination_id=trip_in.destination_id,
        days=trip_in.days,
        travelers_count=trip_in.travelers_count,
        travel_style=trip_in.travel_style,
        total_budget_inr=trip_in.total_budget_inr,
        estimated_cost_inr=trip_in.estimated_cost_inr,
        itinerary_json=trip_in.itinerary
    )
    db.add(trip)
    db.commit()
    db.refresh(trip)
    return trip


@router.get("", response_model=List[TripResponse])
def get_user_trips(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Lists all saved itineraries for the authenticated user."""
    return db.query(Trip).filter(Trip.user_id == current_user.id).order_by(Trip.created_at.desc()).all()


@router.get("/{trip_id}", response_model=TripResponse)
def get_trip_details(
    trip_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieves a specific trip by its ID."""
    trip = db.query(Trip).filter(Trip.id == trip_id, Trip.user_id == current_user.id).first()
    if not trip:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trip not found")
    return trip


@router.delete("/{trip_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_trip(
    trip_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Deletes a saved trip."""
    trip = db.query(Trip).filter(Trip.id == trip_id, Trip.user_id == current_user.id).first()
    if not trip:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trip not found")
    db.delete(trip)
    db.commit()
    return None
