import logging
from typing import Dict, Any
from app.agents.state import TravelState
from app.tools.budget_tools import calculate_trip_budget

logger = logging.getLogger(__name__)


def budget_estimator_agent(state: TravelState) -> Dict[str, Any]:
    """
    Deterministically computes trip expenses across Stay, Food, Activities, Transit,
    and compares against user budget bounds.
    """
    days = max(1, state.get("days", 3))
    travelers_count = max(1, state.get("travelers_count", 1))
    budget_limit = state.get("budget", 0.0)
    hotel = state.get("selected_accommodation") or {}
    hotel_price = hotel.get("price_per_night_inr", 3000.0)
    stay_tier = hotel.get("tier", "Moderate")

    # Sum activity entry fees from day plan
    activities_sum = 0.0
    for day in state.get("day_by_day_plan", []):
        activities_sum += day.get("day_total_cost_inr", 0.0)

    # Tool invocation for deterministic math
    breakdown = calculate_trip_budget.invoke({
        "days": days,
        "travelers_count": travelers_count,
        "stay_tier": stay_tier,
        "hotel_price_per_night": hotel_price,
        "activities_cost": activities_sum,
        "max_budget": budget_limit
    })

    steps = state.get("agent_steps", [])
    status_str = "Within Budget" if breakdown["is_within_budget"] else "Exceeds Budget"
    steps.append({
        "agent": "budget_cost_estimator",
        "status": "completed",
        "output": f"Estimated total: ₹{breakdown['total_estimated_cost_inr']:,.0f} ({status_str}) [Stay: ₹{breakdown['stay_cost_inr']:,.0f}, Food: ₹{breakdown['food_cost_inr']:,.0f}, Transit: ₹{breakdown['transit_cost_inr']:,.0f}]"
    })

    return {
        "cost_breakdown": breakdown,
        "agent_steps": steps
    }
