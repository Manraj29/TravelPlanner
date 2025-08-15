import datetime
from planner_state import PlannerState
from langchain_ollama import ChatOllama

def ask_preferences(state: PlannerState) -> PlannerState:
    llm = ChatOllama(model="llama3.2:3b")  # You can change to llama3, etc.
    # response = llm.invoke(
    #     "Ask the user about their travel preferences: budget, duration, activities, climate preference. Just ask about preferences, do not suggest destinations or anything else."
    # )
    user_input = input("Enter your preferences (budget, duration, activities, climate): ")
    source = input("Enter the departure city: ")
    depart_date = input("Enter the departure date in YYYY-MM-DD format: ")
    duration = int(input("Enter the duration of the trip in days (only number): "))

    state.preferences = user_input.strip() if user_input else None
    state.source = source.strip() if source else None
    state.depart_date = depart_date.strip() if depart_date else None
    state.trip_days = duration if duration else 3

    depart_date_str = state.depart_date
    duration = state.trip_days or 3

    try:
        depart_date = datetime.datetime.strptime(depart_date_str, '%Y-%m-%d')
    except ValueError:
        print("❌ Invalid departure date format.")
        return state

    # Calculate return date
    return_date = depart_date + datetime.timedelta(days=duration)
    return_date_str = return_date.strftime('%Y-%m-%d')
    state.return_date = return_date_str


    print("PREFERENCE: ", state.preferences)
    print("SOURCE: ", state.source)
    print("DEPART DATE: ", state.depart_date)
    print("RETURN DATE: ", state.return_date)
    return state
