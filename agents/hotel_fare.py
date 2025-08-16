import datetime
from planner_state import PlannerState
from tools.hotel_api import format_hotels, get_hotels, get_region_id
from langchain_ollama import ChatOllama

def get_hotel_data(state: PlannerState) -> PlannerState:
    source = state.source
    depart_date = state.depart_date
    return_date = state.return_date
    hotel_specs = state.hotel_specs
    destinations = state.destinations or []
    all_hotels = {}

    print("Source, destination, date, return date", source, destinations, depart_date, return_date, hotel_specs)

    if not source:
        print("❌ No source provided.")
        return state

    llm = ChatOllama(model="llama3.2:3b")

    for dest in destinations:
        dest_id = get_region_id(dest)
        if dest_id:
            print(f"🏨 Searching for hotels in {dest}...")
            hotels = get_hotels(source, dest, depart_date, return_date, dest_id, hotel_specs)
            all_hotels[dest] = format_hotels(hotels)

    print("Hotel DATAS", all_hotels)
    state.hotel_data_raw = all_hotels
    state.hotels = all_hotels

    # SELECT best flights from all
    select_best_hotels(state)
    return state

def select_best_hotels(state: PlannerState) -> PlannerState:
    if not state.hotels:
        print("⚠️ No hotel data to process.")
        return state

    llm = ChatOllama(model="llama3.2:3b")
    best_hotel_summary = {}

    for dest, hotels in state.hotels.items():
        if not hotels or isinstance(hotels, str):
            print(f"⚠️ Skipping destination {dest} due to invalid flight data.")
            continue

        prompt = f"""
        You're a travel assistant helping a user plan a trip.

        The user wants to travel from {state.source} to {dest} between {state.depart_date} and {state.return_date}.
        Their preferences are: {state.preferences}

        Here are the available hotel options in JSON format:
        {hotels}

        Based on these preferences, select the best 1 or 2 hotel options.
        For each, summarize the hotel name, price, rating, ammenities, and location.
        Be clear and concise. DO not suggest any other, or add anything else. Just the best options from the above provided hotels.
        """

        try:
            result = llm.invoke(prompt)
            response = result.content.strip() if hasattr(result, "content") else result
            best_hotel_summary[dest] = response
        except Exception as e:
            best_hotel_summary[dest] = f"⚠️ Error selecting best hotels: {e}"

    state.best_hotels = best_hotel_summary
    return state
