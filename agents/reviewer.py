import datetime
from planner_state import PlannerState
from langchain_ollama import ChatOllama
from tools.saving_file import save_to_file
def plan_trip(state: PlannerState) -> str:
    """Plan a trip based on the given state."""
    with open("output/weather_data.md", "r", encoding="utf-8") as f:
        weather = f.read()
    with open("output/best_hotels.md", "r", encoding="utf-8") as f:
        hotels = f.read()

    with open("output/best_flights.md", "r", encoding="utf-8") as f:
        flights = f.read()

    llm = ChatOllama(model="llama3.2:3b")
    final_prompt = f"""
        You are a helpful travel assistant tasked with planning ideal trip options.

        The user is traveling from **{state.source}**, departing on **{state.depart_date}**, and returning on **{state.return_date}** — a total of **{state.trip_days} days**.
        Their preferences are: **{state.preferences}**

        ---

        ### 🌤 Weather Info (by destination):
        {weather}

        ### ✈️ Flight Options (from source to each destination):
        {flights}

        ### 🏨 Hotel Options (by destination):
        {hotels}

        ---

        ### 📋 TASK:
        For **each destination**, generate a **complete individual trip plan** including:
        - Best flight and hotel selection (based on value, user preferences, and weather).
        - Day-wise itinerary (sightseeing, activities, or weather-dependent suggestions).
        - Summary of trip duration, estimated total cost (flight + hotel), and weather suitability.

        ---

        ### 🔍 COMPARISON:
        At the end, compare all destination plans based on:
        - ✅ Total estimated cost
        - 🌤 Weather conditions
        - 🏷 Value for money
        - 👍 Alignment with user preferences

        Rank the destinations from most to least recommended.

        ---

        ### 📝 FORMAT:
        Respond **only in Markdown** with the following structure:

        ## ✈️ Destination: <City Name>

        **Summary:**
        - Total Cost: $X
        - Weather: Good / Bad / Mixed
        - Flight: <Flight Details>
        - Hotel: <Hotel Details>

        ### 📆 Day-wise Itinerary:
        - **Day 1:** Arrival + activities
        - **Day 2–N:** ...
        - **Last Day:** Return flight

        ---

        ## 🏁 Final Recommendation:
        1. **<Best Destination>** — Reason
        2. ...
        """



    try:
        result = llm.invoke(final_prompt)
        content = result.content.strip()
        print(content)

        save_to_file(content, "trip_plan.md", "Reviewer")
        
        return content
    except Exception as e:
        print("errorr reviewwse: ", e)
        
    