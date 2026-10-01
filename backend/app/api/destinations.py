from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.database.models import Destination, Attraction, Accommodation
from app.database.schemas import DestinationResponse, DestinationDetailResponse, AttractionResponse, AccommodationResponse

router = APIRouter(prefix="/destinations", tags=["Destinations"])


@router.get("", response_model=List[DestinationResponse])
def get_destinations(
    query: Optional[str] = Query(None, description="Search by name, city, country, or tag"),
    continent: Optional[str] = Query(None, description="Filter by continent"),
    db: Session = Depends(get_db)
):
    """Retrieve catalog of destinations with optional filters."""
    q = db.query(Destination)
    if continent:
        q = q.filter(Destination.continent.ilike(f"%{continent}%"))
    if query:
        q = q.filter(
            (Destination.name.ilike(f"%{query}%")) |
            (Destination.country.ilike(f"%{query}%")) |
            (Destination.city.ilike(f"%{query}%")) |
            (Destination.description.ilike(f"%{query}%"))
        )
    return q.all()


@router.get("/{destination_id}", response_model=DestinationDetailResponse)
def get_destination_by_id(destination_id: int, db: Session = Depends(get_db)):
    """Retrieve complete destination details, attractions, and accommodations."""
    dest = db.query(Destination).filter(Destination.id == destination_id).first()
    if not dest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Destination with ID {destination_id} not found"
        )
    return dest


@router.get("/{destination_id}/attractions", response_model=List[AttractionResponse])
def get_destination_attractions(
    destination_id: int,
    category: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Retrieve attractions for a destination with optional category filter."""
    q = db.query(Attraction).filter(Attraction.destination_id == destination_id)
    if category:
        q = q.filter(Attraction.category.ilike(f"%{category}%"))
    return q.all()


@router.get("/{destination_id}/accommodations", response_model=List[AccommodationResponse])
def get_destination_accommodations(
    destination_id: int,
    tier: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Retrieve accommodations for a destination with optional tier filter."""
    q = db.query(Accommodation).filter(Accommodation.destination_id == destination_id)
    if tier:
        q = q.filter(Accommodation.tier.ilike(f"%{tier}%"))
    return q.all()
