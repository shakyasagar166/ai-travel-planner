import logging
from typing import Dict, Any, List
from app.agents.state import TravelState

logger = logging.getLogger(__name__)


def itinerary_scheduling_agent(state: TravelState) -> Dict[str, Any]:
    """
    Creates a detailed day-by-day itinerary with Morning, Afternoon, and Evening slots.
    """
    days = max(1, min(14, state.get("days", 3)))
    attractions = list(state.get("selected_attractions", []))
    matched_dest = state.get("matched_destination")
    dest_name = matched_dest["name"] if matched_dest else "Destination"

    # Group attractions by best time of day if available
    morning_pool = [a for a in attractions if a.get("best_time_of_day") == "Morning"]
    afternoon_pool = [a for a in attractions if a.get("best_time_of_day") == "Afternoon"]
    evening_pool = [a for a in attractions if a.get("best_time_of_day") in ["Evening", "Night"]]

    fallback_pool = attractions.copy()

    days_plan = []
    attr_idx = 0

    for day_num in range(1, days + 1):
        # 1. Morning Slot
        if morning_pool:
            m_attr = morning_pool.pop(0)
            morning = {
                "time": "09:00 AM - 12:30 PM",
                "activity": f"Visit {m_attr['name']}",
                "category": m_attr.get("category", "Sightseeing"),
                "duration_hours": m_attr.get("duration_hours", 2.5),
                "estimated_cost_inr": m_attr.get("entry_fee_inr", 0.0),
                "tips": f"Rating {m_attr.get('rating', 4.5)}/5: {m_attr.get('description')[:120]}..."
            }
        elif fallback_pool:
            m_attr = fallback_pool.pop(0)
            morning = {
                "time": "09:00 AM - 12:30 PM",
                "activity": f"Explore {m_attr['name']}",
                "category": m_attr.get("category", "Sightseeing"),
                "duration_hours": m_attr.get("duration_hours", 2.0),
                "estimated_cost_inr": m_attr.get("entry_fee_inr", 0.0),
                "tips": m_attr.get("description")[:120]
            }
        else:
            morning = {
                "time": "09:00 AM - 12:00 PM",
                "activity": f"Morning walk & breakfast in local market of {dest_name}",
                "category": "Culture & Leisure",
                "duration_hours": 2.5,
                "estimated_cost_inr": 250.0,
                "tips": "Try local breakfast specialties."
            }

        # 2. Afternoon Slot
        if afternoon_pool:
            a_attr = afternoon_pool.pop(0)
            afternoon = {
                "time": "01:30 PM - 04:30 PM",
                "activity": f"Experience {a_attr['name']}",
                "category": a_attr.get("category", "Activities"),
                "duration_hours": a_attr.get("duration_hours", 3.0),
                "estimated_cost_inr": a_attr.get("entry_fee_inr", 0.0),
                "tips": a_attr.get("description")[:120]
            }
        elif fallback_pool:
            a_attr = fallback_pool.pop(0)
            afternoon = {
                "time": "01:30 PM - 04:30 PM",
                "activity": f"Visit {a_attr['name']}",
                "category": a_attr.get("category", "Sightseeing"),
                "duration_hours": a_attr.get("duration_hours", 2.5),
                "estimated_cost_inr": a_attr.get("entry_fee_inr", 0.0),
                "tips": a_attr.get("description")[:120]
            }
        else:
            afternoon = {
                "time": "01:30 PM - 04:30 PM",
                "activity": f"Scenic cafe hopping and relaxation in {dest_name}",
                "category": "Leisure & Dining",
                "duration_hours": 3.0,
                "estimated_cost_inr": 400.0,
                "tips": "Relax and soak in the atmosphere."
            }

        # 3. Evening Slot
        if evening_pool:
            e_attr = evening_pool.pop(0)
            evening = {
                "time": "05:30 PM - 08:30 PM",
                "activity": f"Sunset & evening at {e_attr['name']}",
                "category": e_attr.get("category", "Nightlife & Scenic"),
                "duration_hours": e_attr.get("duration_hours", 3.0),
                "estimated_cost_inr": e_attr.get("entry_fee_inr", 0.0),
                "tips": e_attr.get("description")[:120]
            }
        elif fallback_pool:
            e_attr = fallback_pool.pop(0)
            evening = {
                "time": "05:30 PM - 08:30 PM",
                "activity": f"Evening outing to {e_attr['name']}",
                "category": e_attr.get("category", "Leisure"),
                "duration_hours": e_attr.get("duration_hours", 2.5),
                "estimated_cost_inr": e_attr.get("entry_fee_inr", 0.0),
                "tips": e_attr.get("description")[:120]
            }
        else:
            evening = {
                "time": "06:00 PM - 09:30 PM",
                "activity": f"Dinner & stroll through vibrant street bazaars of {dest_name}",
                "category": "Food & Culture",
                "duration_hours": 3.0,
                "estimated_cost_inr": 600.0,
                "tips": "Enjoy local street delicacies and souvenir shopping."
            }

        day_total = (
            morning["estimated_cost_inr"] +
            afternoon["estimated_cost_inr"] +
            evening["estimated_cost_inr"]
        )

        days_plan.append({
            "day": day_num,
            "title": f"Day {day_num}: Highlights of {dest_name}",
            "morning": morning,
            "afternoon": afternoon,
            "evening": evening,
            "day_total_cost_inr": round(day_total, 2)
        })

    steps = state.get("agent_steps", [])
    steps.append({
        "agent": "itinerary_scheduler",
        "status": "completed",
        "output": f"Constructed cohesive {days}-day timeline (Morning, Afternoon, Evening)"
    })

    return {
        "day_by_day_plan": days_plan,
        "agent_steps": steps
    }
