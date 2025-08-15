from langgraph.graph import StateGraph, END
from planner_state import PlannerState
from agents.preferences import ask_preferences
from agents.destinations import suggest_destinations
from agents.weather import check_weather
from agents.flights_fare import get_flight_data, select_best_flights


# Create graph
graph = StateGraph(PlannerState)

# Add nodes (agents)
graph.add_node("ask_preferences", ask_preferences)
graph.add_node("suggest_destinations", suggest_destinations)
graph.add_node("check_weather", check_weather)
graph.add_node("get_flight_data", get_flight_data)
graph.add_node("select_best_flights", select_best_flights)


# Define flow
graph.set_entry_point("ask_preferences")
graph.add_edge("ask_preferences", "suggest_destinations")
graph.add_edge("suggest_destinations", "get_flight_data")
# graph.add_edge("check_weather", "get_flight_data")
graph.add_edge("get_flight_data", "select_best_flights")
graph.add_edge("select_best_flights", END)


# we can also add conditional edge if we get a place with bad weather we can replace the place with another new place.
# graph.add_conditional_edges(
#     "check_weather",
#     decide_next_step,
#     {
#         "good_weather": END,
#         "bad_weather": "suggest_destinations"
#     }

# )

if __name__ == "__main__":
    compiled = graph.compile()
    result = compiled.invoke(PlannerState())
    print("\n=== Final State ===")
    print(result)
