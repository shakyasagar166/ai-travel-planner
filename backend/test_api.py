import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_api():
    print("\n--- 6. Testing FastAPI REST & Chat Endpoints ---")

    # 1. Health
    res = client.get("/health")
    assert res.status_code == 200
    print(f"[OK] /health: {res.json()}")

    # 2. Destinations
    res = client.get("/api/v1/destinations")
    assert res.status_code == 200
    dests = res.json()
    assert len(dests) >= 8
    print(f"[OK] GET /destinations: retrieved {len(dests)} destinations")

    # 3. Single Destination Detail
    res = client.get(f"/api/v1/destinations/{dests[0]['id']}")
    assert res.status_code == 200
    detail = res.json()
    assert "attractions" in detail
    assert "accommodations" in detail
    print(f"[OK] GET /destinations/{dests[0]['id']}: {detail['name']} with {len(detail['attractions'])} attractions")

    # 4. Auth: Login with Demo User
    res = client.post("/api/v1/auth/login", json={"email": "demo@traveler.com", "password": "Password123!"})
    assert res.status_code == 200
    token_data = res.json()
    token = token_data["access_token"]
    print("[OK] POST /auth/login: Demo login succeeded, JWT token obtained.")

    # 5. Auth Me
    res = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    print(f"[OK] GET /auth/me: {res.json()['full_name']}")

    # 6. Chat Endpoint
    chat_payload = {
        "message": "Plan a 3-day holiday in Manali with snow adventure and cafes for 2 people",
        "conversation_id": None
    }
    res = client.post("/api/v1/chat", json=chat_payload)
    assert res.status_code == 200
    chat_res = res.json()
    assert "conversation_id" in chat_res
    assert "response" in chat_res
    assert "itinerary" in chat_res
    print("[OK] POST /chat: LangGraph agent workflow response received:")
    print(f"   - Conversation ID: {chat_res['conversation_id']}")
    print(f"   - Itinerary Destination: {chat_res['itinerary']['destination']}")
    print(f"   - Agent Steps executed: {len(chat_res['agent_steps'])}")

    print(">>> FastAPI REST & Chat Endpoints Test Passed Successfully!\n")


if __name__ == "__main__":
    test_api()
