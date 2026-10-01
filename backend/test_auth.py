import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from app.core.security import get_password_hash, verify_password, create_access_token, decode_access_token
from app.database.session import SessionLocal
from app.services.auth_service import AuthService
from app.database.schemas import UserRegister, UserLogin


def test_auth():
    print("\n--- 2. Testing Security, Bcrypt Hashing & JWT ---")

    raw_pw = "SecretTrip2026!"
    hashed = get_password_hash(raw_pw)
    assert verify_password(raw_pw, hashed), "Password verification failed"
    assert not verify_password("WrongPassword", hashed), "Invalid password incorrectly passed"
    print("[OK] Password hashing & verification verified.")

    token = create_access_token({"sub": "42", "email": "test@travel.com"})
    assert token, "Token generation failed"
    payload = decode_access_token(token)
    assert payload.get("sub") == "42", "Token payload subject mismatch"
    assert payload.get("email") == "test@travel.com", "Token payload email mismatch"
    print(f"[OK] JWT Token generated & decoded: sub={payload.get('sub')}")

    db = SessionLocal()
    try:
        # Register new unique user
        import uuid
        test_email = f"test_{uuid.uuid4().hex[:6]}@traveler.com"
        reg_data = UserRegister(email=test_email, password="MySecretPassword123", full_name="Test Explorer")
        user = AuthService.register(db, reg_data)
        assert user.id is not None
        print(f"[OK] Registered user via AuthService: {user.email}")

        # Authenticate
        auth_user = AuthService.authenticate(db, test_email, "MySecretPassword123")
        assert auth_user.id == user.id
        print("[OK] AuthService authentication succeeded.")

        print(">>> Authentication & Security Test Passed Successfully!\n")
    finally:
        db.close()


if __name__ == "__main__":
    test_auth()
