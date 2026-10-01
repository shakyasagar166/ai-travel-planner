from typing import List, Optional, Dict, Any
from pydantic import BaseModel, EmailStr, Field


# --- Authentication Schemas ---
class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)
    full_name: str = Field(..., min_length=2)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    is_active: bool

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class TokenPayload(BaseModel):
    sub: Optional[str] = None
    email: Optional[str] = None


# --- Destination & Attraction Schemas ---
class AttractionResponse(BaseModel):
    id: int
    name: str
    category: str
    description: str
    duration_hours: float
    entry_fee_inr: float
    rating: float
    best_time_of_day: str
    image_url: Optional[str] = None

    class Config:
        from_attributes = True


class AccommodationResponse(BaseModel):
    id: int
    name: str
    tier: str
    price_per_night_inr: float
    rating: float
    address: Optional[str] = None
    amenities: List[str] = Field(default_factory=list, alias="amenities_json")
    image_url: Optional[str] = None

    class Config:
        from_attributes = True
        populate_by_name = True


class DestinationResponse(BaseModel):
    id: int
    name: str
    country: str
    city: str
    continent: str
    climate: str
    best_season: str
    currency: str
    avg_daily_budget_inr: float
    description: str
    image_url: Optional[str] = None
    tags: List[str] = Field(default_factory=list, alias="tags_json")

    class Config:
        from_attributes = True
        populate_by_name = True


class DestinationDetailResponse(DestinationResponse):
    attractions: List[AttractionResponse] = []
    accommodations: List[AccommodationResponse] = []


# --- Itinerary & Chat Schemas ---
class ActivityItem(BaseModel):
    time: str
    activity: str
    category: str
    duration_hours: float
    estimated_cost_inr: float
    tips: Optional[str] = None


class DayPlan(BaseModel):
    day: int
    title: str
    morning: ActivityItem
    afternoon: ActivityItem
    evening: ActivityItem
    day_total_cost_inr: float


class CostBreakdown(BaseModel):
    stay_cost_inr: float
    food_cost_inr: float
    activities_cost_inr: float
    transit_cost_inr: float
    total_estimated_cost_inr: float
    budget_limit_inr: float
    is_within_budget: bool
    savings_or_excess_inr: float


class ItineraryPayload(BaseModel):
    destination: str
    days: int
    travelers_count: int
    travel_style: str
    pace: str
    accommodation: Optional[Dict[str, Any]] = None
    cost_breakdown: CostBreakdown
    days_plan: List[DayPlan]
    insider_tips: List[str] = []
    packing_checklist: List[str] = []


class AgentStep(BaseModel):
    agent: str
    status: str = "completed"
    output: str


class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None


class ChatResponse(BaseModel):
    conversation_id: str
    response: str
    itinerary: Optional[ItineraryPayload] = None
    agent_steps: List[AgentStep] = []


# --- Trip Management ---
class TripCreate(BaseModel):
    title: str
    destination_id: int
    days: int
    travelers_count: int = 1
    travel_style: str = "Balanced"
    total_budget_inr: float
    estimated_cost_inr: float
    itinerary: Dict[str, Any]


class TripResponse(BaseModel):
    id: int
    title: str
    destination_id: int
    days: int
    travelers_count: int
    travel_style: str
    total_budget_inr: float
    estimated_cost_inr: float
    itinerary: Dict[str, Any] = Field(alias="itinerary_json")

    class Config:
        from_attributes = True
        populate_by_name = True


# --- User Preferences ---
class UserPreferenceUpdate(BaseModel):
    preferred_travel_style: Optional[str] = "Balanced"
    budget_tier: Optional[str] = "Moderate"
    dietary_preferences: Optional[str] = "Any"
    pace_preference: Optional[str] = "Moderate"
    interests: Optional[List[str]] = []


class UserPreferenceResponse(BaseModel):
    preferred_travel_style: str
    budget_tier: str
    dietary_preferences: str
    pace_preference: str
    interests: List[str] = Field(default_factory=list, alias="interests_json")

    class Config:
        from_attributes = True
        populate_by_name = True
