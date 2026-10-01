from typing import List, Dict, Any, Optional
from langchain_core.tools import tool
from app.rag.retriever import retrieve_travel_knowledge


@tool
def search_travel_knowledge(query: str, destination: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Search indexed travel guides, local insider tips, weather advisories, scams, and packing checklists in ChromaDB.
    """
    return retrieve_travel_knowledge(query=query, destination=destination, top_k=3)
