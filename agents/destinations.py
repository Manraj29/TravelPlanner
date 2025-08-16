import re
from planner_state import PlannerState
from langchain_ollama import ChatOllama
import json

def suggest_destinations(state: PlannerState) -> PlannerState:
    llm = ChatOllama(model="llama3.2:3b")
    preferences = state.preferences or ""

    prompt = f"""
        Suggest 3 travel destinations (proper city name) for someone with the following preferences: {preferences}.
        Return the results as a JSON array of objects, each with:
        - "name": the destination name (it should be a valid city name, official place name, do not shorten the name or anything give the updated city which is valid)
        - "description": a short paragraph on why it's a good fit.
        - "details": this will be a string, details about the destination, including various attractions, activities, and other relevant information. It must be a string in brief 3-4 lines.
        
        DO not assume anything, just return a valid JSON string, no python function or any text before of after the json format.
        Only return valid JSON. No extra commentary like Here are three travel destinations based on your preferences....
    """

    response = llm.invoke(prompt)
    content = response.content.strip()


    if content.startswith("```"):
        content = re.sub(r"^```(?:json)?\s*|\s*```$", "", content.strip(), flags=re.DOTALL)

    print("LLM RESPONSE:", content)

    try:
        destinations_json = json.loads(content)
        keys = [d["name"] for d in destinations_json]

        # Store names for later use (e.g. weather)
        state.destinations = keys
        state.dest_desc = [f"{d['name']} - Description: {d['description']} Details: {d['details']}" for d in destinations_json]

        print("Parsed Destinations:", keys)

    except Exception as e:
        print(f"⚠️ Failed to parse destination JSON: {e}")
        state.destinations = []
        state.dest_desc = {}

    return state
