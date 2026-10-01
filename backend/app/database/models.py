import datetime
from sqlalchemy import (
    Column, Integer, String, Text, Float, Boolean,
    DateTime, ForeignKey, JSON
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    preference = relationship("UserPreference", back_populates="user", uselist=False, cascade="all, delete-orphan")
    trips = relationship("Trip", back_populates="user", cascade="all, delete-orphan")


class Destination(Base):
    __tablename__ = "destinations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    country = Column(String(100), nullable=False, index=True)
    city = Column(String(100), nullable=False, index=True)
    continent = Column(String(50), nullable=False)
    climate = Column(String(100), default="Pleasant")
    best_season = Column(String(255), nullable=False)
    currency = Column(String(10), default="INR")
    avg_daily_budget_inr = Column(Float, nullable=False)
    description = Column(Text, nullable=False)
    image_url = Column(String(500))
    tags_json = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    attractions = relationship("Attraction", back_populates="destination", cascade="all, delete-orphan")
    accommodations = relationship("Accommodation", back_populates="destination", cascade="all, delete-orphan")
    trips = relationship("Trip", back_populates="destination")


class Attraction(Base):
    __tablename__ = "attractions"

    id = Column(Integer, primary_key=True, index=True)
    destination_id = Column(Integer, ForeignKey("destinations.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False, index=True)  # Adventure, Nature, Cultural, Heritage, Food, Nightlife
    description = Column(Text, nullable=False)
    duration_hours = Column(Float, default=2.0)
    entry_fee_inr = Column(Float, default=0.0)
    rating = Column(Float, default=4.5)
    best_time_of_day = Column(String(50), default="Morning")  # Morning, Afternoon, Evening, Night
    image_url = Column(String(500))

    destination = relationship("Destination", back_populates="attractions")


class Accommodation(Base):
    __tablename__ = "accommodations"

    id = Column(Integer, primary_key=True, index=True)
    destination_id = Column(Integer, ForeignKey("destinations.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    tier = Column(String(50), nullable=False, index=True)  # Budget, Moderate, Luxury
    price_per_night_inr = Column(Float, nullable=False)
    rating = Column(Float, default=4.2)
    address = Column(String(255))
    amenities_json = Column(JSON, default=list)
    image_url = Column(String(500))

    destination = relationship("Destination", back_populates="accommodations")


class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True, index=True)
    title = Column(String(255), nullable=False)
    destination_id = Column(Integer, ForeignKey("destinations.id", ondelete="CASCADE"), nullable=False)
    days = Column(Integer, nullable=False)
    travelers_count = Column(Integer, default=1)
    travel_style = Column(String(100), default="Balanced")
    total_budget_inr = Column(Float, nullable=False)
    estimated_cost_inr = Column(Float, nullable=False)
    itinerary_json = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="trips")
    destination = relationship("Destination", back_populates="trips")


class UserPreference(Base):
    __tablename__ = "user_preferences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    preferred_travel_style = Column(String(100), default="Balanced")
    budget_tier = Column(String(50), default="Moderate")
    dietary_preferences = Column(String(255), default="Any")
    pace_preference = Column(String(50), default="Moderate")
    interests_json = Column(JSON, default=list)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    user = relationship("User", back_populates="preference")


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(String(64), primary_key=True, index=True)
    user_id = Column(Integer, nullable=True, index=True)
    title = Column(String(255), default="New Travel Plan")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(String(64), ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False, index=True)
    sender = Column(String(20), nullable=False)  # user, assistant
    content = Column(Text, nullable=False)
    agent_steps_json = Column(JSON, default=list)
    itinerary_json = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    conversation = relationship("Conversation", back_populates="messages")
