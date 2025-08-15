import os
import requests
from dotenv import load_dotenv

load_dotenv()

RAPIDAPI_KEY = os.getenv("RAPID_API_KEY")
FLIGHT_API_HOST = "google-flights2.p.rapidapi.com"

IATA_BASE_URL = "https://google-flights2.p.rapidapi.com/api/v1/searchAirport"
FLIGHT_SEARCH_URL = "https://google-flights2.p.rapidapi.com/api/v1/searchFlights"

HEADERS = {
    "X-RapidAPI-Key": RAPIDAPI_KEY,
    "X-RapidAPI-Host": FLIGHT_API_HOST
}

def get_iata_code(city: str) -> str:
    """Get IATA code for a city."""

    print("searching iata code for ", city)
    querystring = {
        "query": city,
        "language_code":"en-US",
        "country_code":"US"
    }

    response = requests.get(IATA_BASE_URL, headers=HEADERS, params=querystring)
    
    if response.status_code == 200:
        result = response.json()
        # Ensure structure is correct
        if result.get("status") and "data" in result:
            for entry in result["data"]:
                airport_list = entry.get("list", [])
                for airport in airport_list:
                    if airport.get("type") == "airport" and airport.get("id"):
                        return airport["id"]  # Return the first matching airport IATA code
    return "No IATA code found for city: " + city


def get_flights(source_iata: str, dest_iata: str, depart: str, return_date: str) -> list:
    # from depart and return_date remove the time
    depart = depart.split(" ")[0]
    return_date = return_date.split(" ")[0]

    print("searching fligths for ", source_iata, dest_iata, depart, return_date)
    query = {
        "departure_id": source_iata,
        "arrival_id": dest_iata,
        "outbound_date": depart,
        "return_date": return_date,
        "currency":"INR",
    }

    response = requests.get(FLIGHT_SEARCH_URL, headers=HEADERS, params=query)
    if response.status_code == 200:
        # print(response.json())
        return response.json()
    return []

def format_flights(data: dict) -> list:
    try:
        if not data.get("status", False):
            return [{"error": data.get("message", "No flights found.")}]
        
        itineraries = data.get("data", {}).get("itineraries", {})
        top_flights = itineraries.get("topFlights", [])
        
        if not top_flights:
            return [{"message": "No flights available for the selected route and dates."}]

        formatted_flights = []

        for flight_data in top_flights[:5]:
            flight_info = {
                "airline": flight_data.get("flights", [{}])[0].get("airline", "N/A"),
                "flight_number": flight_data.get("flights", [{}])[0].get("flight_number", "N/A"),
                "departure_airport": flight_data.get("flights", [{}])[0].get("departure_airport", {}).get("airport_code", "N/A"),
                "arrival_airport": flight_data.get("flights", [{}])[0].get("arrival_airport", {}).get("airport_code", "N/A"),
                "departure_time": flight_data.get("departure_time", "N/A"),
                "arrival_time": flight_data.get("arrival_time", "N/A"),
                "duration": flight_data.get("duration", {}).get("text", "N/A"),
                "stops": flight_data.get("stops", "N/A"),
                "price": flight_data.get("price", "N/A"),
            }
            formatted_flights.append(flight_info)

        return formatted_flights

    except Exception as e:
        return [{"error": f"Error formatting flights data: {str(e)}"}]

# def format_flights(data: dict) -> dict:
#     """
#     Convert raw API flight data into structured per-destination dict of flight lists.
#     """
#     formatted = {}

#     for destination, raw_data in data.items():
#         if not raw_data.get("status", False):
#             formatted[destination] = [{"error": raw_data.get("message", "No flights found")}]
#             continue

#         itineraries = raw_data.get("data", {}).get("itineraries", {})
#         top_flights = itineraries.get("topFlights", [])

#         flights_list = []

#         for flight_data in top_flights[:5]:
#             flight_info = {
#                 "airline": flight_data.get("flights", [{}])[0].get("airline", "N/A"),
#                 "flight_number": flight_data.get("flights", [{}])[0].get("flight_number", "N/A"),
#                 "departure_airport": flight_data.get("flights", [{}])[0].get("departure_airport", {}).get("airport_code", "N/A"),
#                 "arrival_airport": flight_data.get("flights", [{}])[0].get("arrival_airport", {}).get("airport_code", "N/A"),
#                 "departure_time": flight_data.get("departure_time", "N/A"),
#                 "arrival_time": flight_data.get("arrival_time", "N/A"),
#                 "duration": flight_data.get("duration", {}).get("text", "N/A"),
#                 "stops": flight_data.get("stops", "N/A"),
#                 "price": flight_data.get("price", "N/A"),
#             }
#             flights_list.append(flight_info)

#         formatted[destination] = flights_list

#     return formatted
