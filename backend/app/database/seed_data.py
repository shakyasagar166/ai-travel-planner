import json
import logging
import os
from sqlalchemy.orm import Session
from app.database.models import User, Destination, Attraction, Accommodation, UserPreference
from app.core.security import get_password_hash

logger = logging.getLogger(__name__)


def seed_database(db: Session):
    """
    Seeds database with initial destinations, attractions, hotels, and demo user.
    """
    # 1. Seed Demo User
    demo_user = db.query(User).filter(User.email == "demo@traveler.com").first()
    if not demo_user:
        logger.info("Creating demo user: demo@traveler.com / Password123!")
        demo_user = User(
            email="demo@traveler.com",
            hashed_password=get_password_hash("Password123!"),
            full_name="Explorer Shivam",
            is_active=True
        )
        db.add(demo_user)
        db.flush()

        # Seed default preferences
        pref = UserPreference(
            user_id=demo_user.id,
            preferred_travel_style="Balanced",
            budget_tier="Moderate",
            dietary_preferences="Vegetarian & Street Food",
            pace_preference="Moderate",
            interests_json=["Nature", "Heritage", "Photography", "Cafes"]
        )
        db.add(pref)
        db.commit()

    # 2. Seed Destinations & Attractions
    existing_dest = db.query(Destination).first()
    if existing_dest:
        logger.info("Database destinations already populated. Skipping seed.")
        return

    backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    root_dir = os.path.dirname(backend_dir)
    possible_paths = [
        os.path.join(root_dir, "data", "destinations.json"),
        os.path.join(backend_dir, "data", "destinations.json"),
        os.path.join(os.getcwd(), "data", "destinations.json"),
    ]
    json_path = None
    for p in possible_paths:
        if os.path.exists(p):
            json_path = p
            break

    if not json_path:
        logger.warning(f"Seed file not found in possible locations: {possible_paths}")
        return

    with open(json_path, "r", encoding="utf-8") as f:
        dest_data = json.load(f)

    logger.info(f"Seeding {len(dest_data)} destinations from {json_path}...")
    for item in dest_data:
        dest = Destination(
            name=item["name"],
            country=item["country"],
            city=item["city"],
            continent=item["continent"],
            climate=item.get("climate", "Pleasant"),
            best_season=item["best_season"],
            currency=item.get("currency", "INR"),
            avg_daily_budget_inr=item["avg_daily_budget_inr"],
            description=item["description"],
            image_url=item.get("image_url"),
            tags_json=item.get("tags", [])
        )
        db.add(dest)
        db.flush()

        # Add attractions
        for attr in item.get("attractions", []):
            a = Attraction(
                destination_id=dest.id,
                name=attr["name"],
                category=attr["category"],
                description=attr["description"],
                duration_hours=attr.get("duration_hours", 2.0),
                entry_fee_inr=attr.get("entry_fee_inr", 0.0),
                rating=attr.get("rating", 4.5),
                best_time_of_day=attr.get("best_time_of_day", "Morning"),
                image_url=attr.get("image_url")
            )
            db.add(a)

        # Add accommodations
        for acc in item.get("accommodations", []):
            h = Accommodation(
                destination_id=dest.id,
                name=acc["name"],
                tier=acc["tier"],
                price_per_night_inr=acc["price_per_night_inr"],
                rating=acc.get("rating", 4.2),
                address=acc.get("address"),
                amenities_json=acc.get("amenities", []),
                image_url=acc.get("image_url")
            )
            db.add(h)

    db.commit()
    logger.info("Destination catalog successfully seeded!")
