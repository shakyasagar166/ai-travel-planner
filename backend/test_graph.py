import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from app.graph.travel_graph import travel_app


def test_graph():
    print("\n--- 5. Testing LangGraph Multi-Agent Workflow ---")

    test_query = "Plan a 4-day budget trip to Goa for 2 people with Rs. 35,000 budget. We love beaches, water sports, and sunset shacks."
    print(f"User Query: '{test_query}'\n")

    initial_state = {
        "user_query": test_query,
        "user_id": 1,
        "agent_steps": []
    }

    final_state = travel_app.invoke(initial_state)

    print("--- Executed Multi-Agent Steps ---")
    for step in final_state.get("agent_steps", []):
        print(f"-> [{step['agent']}]: {step['output']}")

    assert final_state.get("destination") == "Goa", f"Expected Goa, got {final_state.get('destination')}"
    assert final_state.get("days") == 4, f"Expected 4 days, got {final_state.get('days')}"
    assert len(final_state.get("day_by_day_plan", [])) == 4, "Expected 4 days in schedule"
    assert final_state.get("cost_breakdown") is not None, "Cost breakdown missing"
    assert final_state.get("itinerary_payload") is not None, "Itinerary payload missing"

    payload = final_state.get("itinerary_payload")
    print(f"\n[OK] Itinerary generated for: {payload['destination']}")
    print(f"[OK] Total Estimated Cost: Rs. {payload['cost_breakdown']['total_estimated_cost_inr']:,.0f}")
    print(f"[OK] Days in timeline: {len(payload['days_plan'])}")
    print(f"[OK] Recommended stay: {payload['accommodation']['name']}")

    print(">>> LangGraph Multi-Agent Workflow Test Passed Successfully!\n")


if __name__ == "__main__":
    test_graph()
