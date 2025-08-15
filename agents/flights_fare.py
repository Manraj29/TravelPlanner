import datetime
from planner_state import PlannerState
from tools.flight_api import format_flights, get_flights, get_iata_code
from langchain_ollama import ChatOllama

def get_flight_data(state: PlannerState) -> PlannerState:

    source = state.source
    depart_date = state.depart_date
    return_date = state.return_date
    destinations = state.destinations or []
    all_flights = {}
    flight_data = {}

    print("Source, destination, date, return date", source, destinations, depart_date, return_date)

    if not source:
        print("❌ No source provided.")
        return state

    source_iata = get_iata_code(source)
    if not source_iata:
        print(f"❌ Failed to find IATA for source: {source}")
        return state
    llm = ChatOllama(model="llama3.2:3b")

    for dest in destinations:
        dest_iata = get_iata_code(dest)
        if not dest_iata:
            print(f"⚠️ Skipping {dest} (IATA not found)")
            prompt = f"""
                Please provide the IATA code for {dest}. Just return the valid official IATA code. Nothing else.
                """
            result = llm.invoke(prompt)
            return_date = result['output']
            continue

        flights = get_flights(source_iata, dest_iata, depart_date, return_date)
        all_flights[dest] = format_flights(flights)
    
    print("FLIGHT DATAS", all_flights)
    state.flight_data_raw = all_flights
    state.flights = all_flights
    return state


def select_best_flights(state: PlannerState) -> PlannerState:
    if not state.flights:
        print("⚠️ No flight data to process.")
        return state

    llm = ChatOllama(model="llama3.2:3b")
    best_flights_summary = {}

    for dest, flights in state.flights.items():
        if not flights or isinstance(flights, str):
            print(f"⚠️ Skipping destination {dest} due to invalid flight data.")
            continue

        prompt = f"""
        You're a travel assistant helping a user plan a trip.

        The user wants to travel from {state.source} to {dest} between {state.depart_date} and {state.return_date}.
        Their preferences are: {state.preferences}

        Here are the available flight options in JSON format:
        {flights}

        Based on these preferences, select the best 1 or 2 flight options.
        For each, summarize the airline, price, duration, stops, and departure time.

        Be clear and concise.
        """

        try:
            result = llm.invoke(prompt)
            response = result.content.strip() if hasattr(result, "content") else result
            best_flights_summary[dest] = response
        except Exception as e:
            best_flights_summary[dest] = f"⚠️ Error selecting best flights: {e}"

    state.best_flights = best_flights_summary
    return state
