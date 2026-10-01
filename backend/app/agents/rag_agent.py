import logging
from typing import Dict, Any, List
from app.agents.state import TravelState
from app.rag.retriever import retrieve_travel_knowledge, format_travel_context

logger = logging.getLogger(__name__)


def travel_knowledge_rag_agent(state: TravelState) -> Dict[str, Any]:
    """
    Retrieves dense semantic knowledge from ChromaDB: local customs, weather warnings,
    culinary recommendations, and transit tips.
    """
    matched_dest = state.get("matched_destination")
    dest_name = matched_dest["name"] if matched_dest else state.get("destination", "Goa")
    user_query = state.get("user_query", "")

    # Retrieve relevant travel knowledge from ChromaDB
    chunks = retrieve_travel_knowledge(
        query=f"{user_query} {dest_name} weather travel tips safety food",
        destination=dest_name,
        top_k=3
    )

    rag_text = format_travel_context(chunks)

    # Extract tips and packing suggestions
    insider_tips = []
    if matched_dest:
        dest_tags = [t.lower() for t in matched_dest.get("tags", [])]
        if "beach" in dest_tags:
            insider_tips.extend([
                "Rent a two-wheeler for scenic coastal flexibility.",
                "Try local fresh seafood shacks away from crowded tourist strips.",
                "Carry high SPF sunscreen and hydrate frequently in coastal heat."
            ])
            packing = ["Swimwear & quick-dry towels", "Sunglasses & Sunscreen SPF 50+", "Flip flops & waterproof phone pouch", "Light cotton clothes"]
        elif "mountains" in dest_tags:
            insider_tips.extend([
                "Layer up — temperatures drop drastically after sunset.",
                "Pre-book high-altitude passes or vehicle permits 3 days in advance.",
                "Acclimatize properly and drink plenty of warm water."
            ])
            packing = ["Thermal inners & fleece jacket", "Waterproof trekking shoes", "Lip balm & moisturizer", "Woolen socks & gloves"]
        elif "modern" in dest_tags or "anime" in dest_tags:
            insider_tips.extend([
                "Get a digital transit IC card on your phone for frictionless metro travel.",
                "Carry a pocket WiFi or travel eSIM for uninterrupted navigation.",
                "Many classic eateries are cash-only; carry local currency."
            ])
            packing = ["Comfortable walking sneakers (15,000+ steps/day)", "Universal power adapter", "Compact umbrella", "Power bank"]
        else:
            insider_tips.extend([
                "Opt for morning hours for landmark visits to beat the midday sun and crowds.",
                "Sample famous local street food at bustling night markets.",
                "Bargain respectfully in local artisan bazaars."
            ])
            packing = ["Breathable cotton outfits", "Comfortable walking shoes", "Hand sanitizer & wet wipes", "Power bank"]
    else:
        insider_tips = ["Always carry a photocopy of your travel IDs.", "Keep offline maps downloaded."]
        packing = ["Comfortable clothes", "Walking shoes", "Personal medication", "Chargers & power bank"]

    steps = state.get("agent_steps", [])
    steps.append({
        "agent": "travel_knowledge_rag",
        "status": "completed",
        "output": f"Retrieved {len(chunks)} verified insider guides and localized safety advisories from ChromaDB"
    })

    return {
        "rag_context": rag_text,
        "insider_tips": insider_tips,
        "packing_checklist": packing,
        "agent_steps": steps
    }
