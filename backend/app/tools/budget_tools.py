from typing import Dict, Any
from langchain_core.tools import tool


@tool
def calculate_trip_budget(
    days: int,
    travelers_count: int,
    stay_tier: str,
    hotel_price_per_night: float,
    activities_cost: float,
    max_budget: float
) -> Dict[str, Any]:
    """
    Deterministically calculates trip costs: Stay, Food, Activities, Local Transit, and verifies against user budget.
    """
    days = max(1, days)
    travelers_count = max(1, travelers_count)
    nights = max(1, days - 1) if days > 1 else 1

    # Tier multipliers for daily food & local transit
    tier_lower = stay_tier.lower()
    if "luxury" in tier_lower:
        daily_food_per_person = 3000.0
        daily_transit_per_person = 1500.0
    elif "moderate" in tier_lower or "comfort" in tier_lower:
        daily_food_per_person = 1400.0
        daily_transit_per_person = 700.0
    else:  # Budget
        daily_food_per_person = 700.0
        daily_transit_per_person = 350.0

    stay_total = round(nights * hotel_price_per_night, 2)
    food_total = round(days * travelers_count * daily_food_per_person, 2)
    transit_total = round(days * travelers_count * daily_transit_per_person, 2)
    activities_total = round(activities_cost * travelers_count, 2)

    total_estimated = round(stay_total + food_total + transit_total + activities_total, 2)
    is_within = (max_budget <= 0) or (total_estimated <= max_budget)
    diff = round(max_budget - total_estimated, 2) if max_budget > 0 else 0.0

    return {
        "stay_cost_inr": stay_total,
        "food_cost_inr": food_total,
        "transit_cost_inr": transit_total,
        "activities_cost_inr": activities_total,
        "total_estimated_cost_inr": total_estimated,
        "budget_limit_inr": max_budget,
        "is_within_budget": is_within,
        "savings_or_excess_inr": diff
    }
