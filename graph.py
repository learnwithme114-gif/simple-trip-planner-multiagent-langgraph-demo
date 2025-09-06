from langgraph.graph import StateGraph, START, END
from state import TripState
from agents import orchestrator, flights_agent, hotels_agent, calendar_agent, integrator

graph = StateGraph(TripState)

graph.add_node("orchestrator", orchestrator)
graph.add_node("flights", flights_agent)
graph.add_node("hotels", hotels_agent)
graph.add_node("calendar", calendar_agent)
graph.add_node("integrator", integrator)

graph.add_edge(START, "orchestrator")
graph.add_edge("orchestrator", "flights")
graph.add_edge("orchestrator", "hotels")
graph.add_edge("orchestrator", "calendar")
graph.add_edge("flights", "integrator")
graph.add_edge("hotels", "integrator")
graph.add_edge("calendar", "integrator")
graph.add_edge("integrator", END)

app = graph.compile()
