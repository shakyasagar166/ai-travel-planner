import logging
from typing import Dict, Any
from langchain_core.messages import SystemMessage, HumanMessage
from app.agents.state import TravelState
from app.agents.llm import get_llm

logger = logging.getLogger(__name__)


def final_itinerary_agent(state: TravelState) -> Dict[str, Any]:
    """
    Synthesizes a cohesive final travel narrative and constructs the typed
    ItineraryPayload for the React frontend.
    """
    matched_dest = state.get("matched_destination") or {}
    dest_name = matched_dest.get("name", state.get("destination", "Your Destination"))
    days = state.get("days", 3)
    travelers = state.get("travelers_count", 1)
    budget = state.get("budget", 0.0)
    travel_style = state.get("travel_style", "Balanced")
    pace = state.get("pace", "Moderate")

    hotel = state.get("selected_accommodation") or {}
    breakdown = state.get("cost_breakdown") or {}
    days_plan = state.get("day_by_day_plan") or []
    insider_tips = state.get("insider_tips") or []
    packing_checklist = state.get("packing_checklist") or []
    rag_context = state.get("rag_context", "")

    # Build typed payload for Frontend
    itinerary_payload = {
        "destination": dest_name,
        "days": days,
        "travelers_count": travelers,
        "travel_style": travel_style,
        "pace": pace,
        "accommodation": hotel,
        "cost_breakdown": breakdown,
        "days_plan": days_plan,
        "insider_tips": insider_tips,
        "packing_checklist": packing_checklist
    }

    # Generate Markdown Narrative
    llm = get_llm(temperature=0.4)
    final_text = ""

    if llm:
        system_prompt = (
            "You are an Elite AI Travel Concierge. "
            "Write an engaging, well-formatted markdown response presenting the customized itinerary to the traveler.\n"
            "Include:\n"
            "1. An enthusiastic trip intro tailored to their travel style and destination.\n"
            "2. Summary of their stay and estimated budget breakdown.\n"
            "3. Key daily itinerary highlights.\n"
            "4. Essential local travel tips & packing advice."
        )
        user_prompt = (
            f"Destination: {dest_name}\n"
            f"Duration: {days} Days, Travelers: {travelers}\n"
            f"Style: {travel_style}, Pace: {pace}\n"
            f"Accommodation: {hotel.get('name')} (₹{hotel.get('price_per_night_inr')}/night)\n"
            f"Total Estimated Budget: ₹{breakdown.get('total_estimated_cost_inr', 0):,.0f} "
            f"(User Budget: ₹{budget:,.0f})\n"
            f"Days Plan Summary: {len(days_plan)} days scheduled.\n"
            f"Context: {rag_context[:300]}"
        )
        try:
            res = llm.invoke([SystemMessage(content=system_prompt), HumanMessage(content=user_prompt)])
            final_text = res.content.strip()
        except Exception as e:
            logger.warning(f"LLM final synthesis error: {e}. Falling back to template.")

    if not final_text:
        budget_status = "within your specified budget" if breakdown.get("is_within_budget", True) else "slightly exceeds target budget"
        final_text = (
            f"### ✈️ Your Custom {days}-Day Itinerary for {dest_name}!\n\n"
            f"We've tailored a **{travel_style}** journey for **{travelers} traveler{'s' if travelers > 1 else ''}**.\n\n"
            f"#### 🏨 Recommended Stay\n"
            f"**{hotel.get('name', 'Curated Hotel')}** ({hotel.get('tier', 'Moderate')} Tier) — ₹{hotel.get('price_per_night_inr', 3000):,.0f}/night\n\n"
            f"#### 💰 Budget Estimate\n"
            f"* **Total Estimated Cost**: ₹{breakdown.get('total_estimated_cost_inr', 0):,.0f} ({budget_status})\n"
            f"* **Accommodation**: ₹{breakdown.get('stay_cost_inr', 0):,.0f}\n"
            f"* **Food & Dining**: ₹{breakdown.get('food_cost_inr', 0):,.0f}\n"
            f"* **Activities & Entry Tickets**: ₹{breakdown.get('activities_cost_inr', 0):,.0f}\n"
            f"* **Local Transit**: ₹{breakdown.get('transit_cost_inr', 0):,.0f}\n\n"
            f"Check out the interactive Day-by-Day timeline and budget cards below!"
        )

    steps = state.get("agent_steps", [])
    steps.append({
        "agent": "final_response_synthesis",
        "status": "completed",
        "output": f"Compiled complete travel itinerary and structured UI cards for {dest_name}"
    })

    return {
        "final_response": final_text,
        "itinerary_payload": itinerary_payload,
        "agent_steps": steps
    }
