import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from app.tools.destination_tools import search_destinations, get_destination_details
from app.tools.attraction_tools import search_attractions, filter_attractions_by_interests
from app.tools.accommodation_tools import search_accommodations
from app.tools.budget_tools import calculate_trip_budget


def test_tools():
    print("\n--- 4. Testing LangChain Tool Calling Layer ---")

    # 1. search_destinations
    dests = search_destinations.invoke({"query": "Goa"})
    assert len(dests) > 0, "Failed to search destinations"
    print(f"[OK] search_destinations found: {dests[0]['name']}")

    # 2. search_attractions
    attrs = search_attractions.invoke({"destination_name": "Goa"})
    assert len(attrs) > 0, "Failed to search attractions"
    print(f"[OK] search_attractions found {len(attrs)} spots in Goa")

    # 3. filter_attractions_by_interests
    filtered = filter_attractions_by_interests.invoke({"destination_id": dests[0]["id"], "interests": ["beach", "water sports"]})
    assert len(filtered) > 0, "Failed to filter attractions"
    print(f"[OK] filter_attractions_by_interests top spot: {filtered[0]['name']}")

    # 4. search_accommodations
    hotels = search_accommodations.invoke({"destination_name": "Goa", "tier": "Moderate"})
    assert len(hotels) > 0, "Failed to search accommodations"
    print(f"[OK] search_accommodations found: {hotels[0]['name']} (Rs. {hotels[0]['price_per_night_inr']}/night)")

    # 5. calculate_trip_budget
    budget_res = calculate_trip_budget.invoke({
        "days": 4,
        "travelers_count": 2,
        "stay_tier": "Moderate",
        "hotel_price_per_night": 4200,
        "activities_cost": 2500,
        "max_budget": 50000
    })
    assert budget_res["total_estimated_cost_inr"] > 0
    print(f"[OK] calculate_trip_budget total: Rs. {budget_res['total_estimated_cost_inr']:,.0f}, Within: {budget_res['is_within_budget']}")

    print(">>> Tool Calling Layer Test Passed Successfully!\n")


if __name__ == "__main__":
    test_tools()
