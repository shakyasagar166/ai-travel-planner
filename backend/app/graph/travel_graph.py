import logging
from langgraph.graph import StateGraph, START, END
from app.agents.state import TravelState
from app.agents.requirement_agent import requirement_understanding_agent
from app.agents.supervisor_agent import supervisor_agent
from app.agents.destination_agent import destination_agent
from app.agents.attraction_agent import attraction_agent
from app.agents.accommodation_agent import accommodation_agent
from app.agents.itinerary_agent import itinerary_scheduling_agent
from app.agents.budget_agent import budget_estimator_agent
from app.agents.rag_agent import travel_knowledge_rag_agent
from app.agents.final_agent import final_itinerary_agent

logger = logging.getLogger(__name__)


def build_travel_graph():
    """
    Constructs and compiles the full LangGraph multi-agent travel orchestration mesh.
    """
    workflow = StateGraph(TravelState)

    # 1. Register Nodes
    workflow.add_node("requirement_agent", requirement_understanding_agent)
    workflow.add_node("supervisor_agent", supervisor_agent)
    workflow.add_node("destination_agent", destination_agent)
    workflow.add_node("attraction_agent", attraction_agent)
    workflow.add_node("accommodation_agent", accommodation_agent)
    workflow.add_node("itinerary_agent", itinerary_scheduling_agent)
    workflow.add_node("budget_agent", budget_estimator_agent)
    workflow.add_node("rag_agent", travel_knowledge_rag_agent)
    workflow.add_node("final_agent", final_itinerary_agent)

    # 2. Define Execution Graph Edges
    workflow.add_edge(START, "requirement_agent")
    workflow.add_edge("requirement_agent", "supervisor_agent")
    workflow.add_edge("supervisor_agent", "destination_agent")
    workflow.add_edge("destination_agent", "attraction_agent")
    workflow.add_edge("attraction_agent", "accommodation_agent")
    workflow.add_edge("accommodation_agent", "itinerary_agent")
    workflow.add_edge("itinerary_agent", "budget_agent")
    workflow.add_edge("budget_agent", "rag_agent")
    workflow.add_edge("rag_agent", "final_agent")
    workflow.add_edge("final_agent", END)

    compiled = workflow.compile()
    logger.info("Compiled LangGraph Travel Planner workflow successfully.")
    return compiled


travel_app = build_travel_graph()
