from typing import Dict
from planner_state import PlannerState
from tools.weather_api import format_weather, get_weather

MAX_ATTEMPTS = 1

def check_weather(state: PlannerState) -> PlannerState:
    """Check weather for each destination and update state."""
    weather_results: Dict[str, str] = {}
    state.attempts += 1
    
    print("DESTINATIONS ", state.destinations)
    if not state.destinations:
        return state

    for dest in state.destinations:
        print(f"getting weather for {dest}")
        weather_data = get_weather(dest)
        if "error" not in weather_data:
            formatted = format_weather(weather_data)
            weather_results[dest] = formatted
        else:
            weather_results[dest] = f"❌ Could not fetch weather for {dest}."

    state.weather_data = weather_results
    print("WEATHER STATE: ", state.weather_data)
    return state

def weather_is_good(state: PlannerState) -> bool:
    """Check if at least one destination has good weather (20–30°C)."""
    if not state.weather_data:
        return False

    for report in state.weather_data.values():
        if "🌡️ Temperature" in report:
            try:
                temp_str = report.split("🌡️ Temperature: ")[1].split("°C")[0]
                temp = float(temp_str)
                if 20 <= temp <= 30:
                    return True
            except:
                continue

    return False


def decide_next_step(state: PlannerState) -> str:
    if weather_is_good(state):
        return "good_weather"
    elif state.attempts >= MAX_ATTEMPTS:
        print("⚠️ Max attempts reached. Proceeding anyway.")
        return "good_weather"
    else:
        return "bad_weather"
