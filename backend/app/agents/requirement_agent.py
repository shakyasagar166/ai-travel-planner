import json
import logging
import re
from typing import Dict, Any
from langchain_core.messages import SystemMessage, HumanMessage
from app.agents.state import TravelState
from app.agents.llm import get_llm

logger = logging.getLogger(__name__)


def requirement_understanding_agent(state: TravelState) -> Dict[str, Any]:
    """
    Parses natural language query into typed travel parameters:
    destination, days, budget, travelers_count, travel_style, interests, pace.
    """
    query = state.get("user_query", "")
    llm = get_llm(temperature=0.0)

    requirements = {}

    if llm:
        system_prompt = (
            "You are a Travel Requirement Extraction Specialist. "
            "Analyze the user's travel request and extract the following parameters as strict JSON:\n"
            "- destination: (string, e.g. 'Goa', 'Tokyo', 'Manali', 'Paris', etc. or null)\n"
            "- days: (integer, default 3)\n"
            "- budget: (number in INR, default 0 if not mentioned)\n"
            "- travelers_count: (integer, default 1)\n"
            "- travel_style: (e.g. 'Adventure', 'Relaxed', 'Cultural', 'Foodie', 'Luxury', 'Budget', 'Balanced')\n"
            "- interests: (list of strings, e.g. ['beach', 'nightlife', 'hiking'])\n"
            "- pace: ('Relaxed', 'Moderate', 'Fast-paced')\n"
            "Return ONLY a valid JSON object."
        )
        try:
            res = llm.invoke([SystemMessage(content=system_prompt), HumanMessage(content=query)])
            raw_text = res.content.strip()
            if "```" in raw_text:
                raw_text = raw_text.split("```")[1]
                if raw_text.startswith("json"):
                    raw_text = raw_text[4:].strip()
            requirements = json.loads(raw_text)
        except Exception as e:
            logger.warning(f"LLM requirement parsing error: {e}. Utilizing regex fallback.")

    # Fallback / Deterministic Extraction
    if not requirements or not requirements.get("destination"):
        q_lower = query.lower()

        # Destination Detection
        known_destinations = ["goa", "manali", "jaipur", "kerala", "munnar", "alleppey", "tokyo", "paris", "bali", "dubai"]
        detected_dest = None
        for d in known_destinations:
            if d in q_lower:
                detected_dest = "Kerala" if d in ["munnar", "alleppey"] else d.title()
                break

        # Days Detection (e.g. "5 days", "4-day", "a week", "weekend")
        days = 3
        days_match = re.search(r'(\d+)\s*(?:-|\s)?\s*(?:days?|nights?)', q_lower)
        if days_match:
            days = min(14, max(1, int(days_match.group(1))))
        elif "week" in q_lower:
            days = 7
        elif "weekend" in q_lower:
            days = 2

        # Budget Detection (e.g. "under 50k", "Rs. 35,000 budget", "₹40,000", "30k")
        budget = 0.0
        b_match = (
            re.search(r'(?:rs\.?|inr|₹)\s*(\d+(?:,\d+)*(?:\.\d+)?)\s*(k|thousand|lakh|lac)?', q_lower) or
            re.search(r'(?:budget|cost|max|under|around)\s*(?:of|is|:)?\s*(?:rs\.?|inr|₹)?\s*(\d+(?:,\d+)*(?:\.\d+)?)\s*(k|thousand|lakh|lac)?', q_lower) or
            re.search(r'(\d+(?:,\d+)*(?:\.\d+)?)\s*(k|thousand|lakh|lac)\s*(?:budget|inr|rs)?', q_lower)
        )
        if b_match:
            num_str = b_match.group(1).replace(",", "")
            multiplier = b_match.group(2) if len(b_match.groups()) > 1 else None
            try:
                base_num = float(num_str)
                if multiplier in ["k", "thousand"]:
                    budget = base_num * 1000
                elif multiplier in ["lakh", "lac"]:
                    budget = base_num * 100000
                else:
                    budget = base_num
            except Exception:
                budget = 0.0

        # Travelers count (e.g. "2 people", "couple", "family of 4", "solo", "friends")
        travelers = 1
        if "couple" in q_lower or "partner" in q_lower or "2 people" in q_lower or "two of us" in q_lower:
            travelers = 2
        elif "solo" in q_lower:
            travelers = 1
        elif "family" in q_lower:
            travelers = 4
        else:
            t_match = re.search(r'(\d+)\s*(?:people|persons?|travelers?|friends?)', q_lower)
            if t_match:
                travelers = int(t_match.group(1))

        # Travel Style & Interests
        interests = []
        if any(w in q_lower for w in ["beach", "sea", "ocean", "swim"]):
            interests.append("beach")
        if any(w in q_lower for w in ["party", "nightlife", "club", "pub"]):
            interests.append("nightlife")
        if any(w in q_lower for w in ["hike", "trek", "mountain", "snow", "paraglid"]):
            interests.append("adventure")
        if any(w in q_lower for w in ["fort", "palace", "temple", "monument", "history", "museum"]):
            interests.append("heritage")
        if any(w in q_lower for w in ["food", "cuisine", "eat", "cafe", "restaurant", "tasting"]):
            interests.append("foodie")
        if any(w in q_lower for w in ["relax", "peace", "spa", "backwater", "yoga"]):
            interests.append("relaxation")

        travel_style = "Balanced"
        if "adventure" in interests:
            travel_style = "Adventure"
        elif "nightlife" in interests:
            travel_style = "Nightlife & Leisure"
        elif "relaxation" in interests:
            travel_style = "Relaxed & Wellness"
        elif "heritage" in interests:
            travel_style = "Cultural Heritage"

        requirements = {
            "destination": detected_dest or "Goa",
            "days": days,
            "budget": budget,
            "travelers_count": travelers,
            "travel_style": travel_style,
            "interests": interests or ["sightseeing", "relaxation"],
            "pace": "Moderate"
        }

    steps = state.get("agent_steps", [])
    steps.append({
        "agent": "requirement_understanding",
        "status": "completed",
        "output": f"Parsed destination: {requirements.get('destination')}, Duration: {requirements.get('days')} days, Budget: ₹{requirements.get('budget', 0):,.0f}"
    })

    return {
        "destination": requirements.get("destination"),
        "days": int(requirements.get("days", 3)),
        "budget": float(requirements.get("budget", 0)),
        "travelers_count": int(requirements.get("travelers_count", 1)),
        "travel_style": requirements.get("travel_style", "Balanced"),
        "interests": requirements.get("interests", []),
        "pace": requirements.get("pace", "Moderate"),
        "extracted_requirements": requirements,
        "agent_steps": steps
    }
