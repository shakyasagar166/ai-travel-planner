import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from app.database.session import init_db, SessionLocal
from app.database.models import Destination, Attraction, Accommodation, User
from app.database.seed_data import seed_database


def test_database():
    print("\n--- 1. Testing Database Initialization & Models ---")
    init_db()
    db = SessionLocal()
    try:
        seed_database(db)

        # Verify destinations
        dest_count = db.query(Destination).count()
        print(f"[OK] Destinations count: {dest_count}")
        assert dest_count >= 8, f"Expected at least 8 destinations, got {dest_count}"

        # Verify attractions
        attr_count = db.query(Attraction).count()
        print(f"[OK] Attractions count: {attr_count}")
        assert attr_count >= 20, f"Expected at least 20 attractions, got {attr_count}"

        # Verify stays
        acc_count = db.query(Accommodation).count()
        print(f"[OK] Accommodations count: {acc_count}")
        assert acc_count >= 15, f"Expected at least 15 accommodations, got {acc_count}"

        # Verify demo user
        user = db.query(User).filter(User.email == "demo@traveler.com").first()
        assert user is not None, "Demo user not found"
        print(f"[OK] Demo user verified: {user.email} (ID: {user.id})")

        print(">>> Database Models & Seeding Test Passed Successfully!\n")
    finally:
        db.close()


if __name__ == "__main__":
    test_database()
