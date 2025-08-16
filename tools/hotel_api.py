import os
import requests
from dotenv import load_dotenv

load_dotenv()

RAPIDAPI_KEY = os.getenv("RAPID_API_KEY")
HOTEL_API_HOST = "hotels-com-provider.p.rapidapi.com"

HOTEL_SEARCH_URL = "https://hotels-com-provider.p.rapidapi.com/v2/hotels/search"
HOTEL_REGION_URL = "https://hotels-com-provider.p.rapidapi.com/v2/regions"

HEADERS = {
    "X-RapidAPI-Key": RAPIDAPI_KEY,
    "X-RapidAPI-Host": HOTEL_API_HOST
}

import requests

def get_region_id(city: str) -> str:
    """Get region id for a city."""

    print("Searching region id for", city)
    querystring = {
        "query": city,
        "domain":"US",
        "locale":"en_US"
    }

    try:
        response = requests.get(HOTEL_REGION_URL, headers=HEADERS, params=querystring)
        print("Status code:", response.status_code)

        if response.status_code == 200:
            result = response.json()

            if "data" in result and result["data"]:
                for entry in result["data"]:
                    if entry.get("type") == "CITY":
                        print("Found CITY:", entry.get("gaiaId"))
                        return entry.get("gaiaId")

                # Fall back to first gaiaId if CITY type not found
                print("Falling back to first entry:", result["data"][0].get("gaiaId"))
                return result["data"][0].get("gaiaId")
            else:
                print("No data found in result")
        else:
            print("Non-200 response:", response.status_code, response.text)

    except requests.exceptions.RequestException as e:
        print("Request failed:", str(e))
    except ValueError as e:
        print("Failed to parse JSON:", str(e))
    except Exception as e:
        print("Unexpected error:", str(e))

    return "No region id found for city: " + city

import requests

def get_hotels(source: str, dest: str, depart: str, return_date: str, dest_id: int, hotel_specs: str) -> list:
    # From depart and return_date remove the time
    depart = depart.split(" ")[0]
    return_date = return_date.split(" ")[0]

    # Convert hotel specs to dictionary
    hotel_specs_dict = {}
    for spec in hotel_specs.replace(" ", "").split(","):
        parts = spec.split(":")
        if len(parts) == 2:
            hotel_specs_dict[parts[0]] = parts[1]

    print("Searching hotels for:", source, dest, depart, return_date, dest_id)
    # print("Hotel specs dict:", hotel_specs_dict)

    querystring = {
        "amenities": hotel_specs_dict.get("amenities") or "WIFI,POOL,GYM",
        "meal_plan": hotel_specs_dict.get("meal_plan") or "FREE_BREAKFAST",
        "guest_rating_min": hotel_specs_dict.get("guest_rating_min", 8),
        "checkin_date": depart,
        "checkout_date": return_date,
        "lodging_type": hotel_specs_dict.get("lodging_type") or "HOTEL",
        "region_id": dest_id,
        "available_filter": "SHOW_AVAILABLE_ONLY",
        "currency": "USD",
        "sort_order": "DISTANCE",
        "adults_number": hotel_specs_dict.get("adults_number", 1),
        "locale": "es_US",
        "domain": "US",
    }

    try:
        response = requests.get(HOTEL_SEARCH_URL, headers=HEADERS, params=querystring)
        print("Status code:", response.status_code)

        if response.status_code == 200:
            data = response.json()
            print("Hotel search result:", data)
            return data
        else:
            print("Non-200 response:", response.status_code, response.text)

    except requests.exceptions.RequestException as e:
        print("Request failed:", str(e))
    except ValueError as e:
        print("Failed to parse JSON:", str(e))
    except Exception as e:
        print("Unexpected error:", str(e))

    return []
def format_hotels(data: dict) -> list:
    try:
        # Step 1: Access properties list
        properties = data.get("properties", [])
        if not properties:
            return [{"message": "No hotels available for the selected region and dates."}]

        formatted_hotels = []

        # Step 2: Format each property
        for hotel in properties[:4]:  # Limit to top 5
            name = hotel.get("name", "N/A")
            stars = hotel.get("star", "N/A")
            neighborhood = hotel.get("neighborhood", {}).get("name", "N/A")
            region_id = hotel.get("regionId", "N/A")

            # Availability
            availability = hotel.get("availability", {})
            available = availability.get("available", False)
            min_rooms_left = availability.get("minRoomsLeft")
            availability_str = "Available"
            if available and min_rooms_left:
                availability_str += f" ({min_rooms_left} rooms left)"
            elif not available:
                availability_str = "Not Available"

            # Price
            price_options = hotel.get("price", {}).get("options", [])
            display_price = price_options[0].get("formattedDisplayPrice") if price_options else "N/A"

            # Price description (e.g., for 3 nights, Aug 16 - Aug 19)
            price_messages = hotel.get("price", {}).get("priceMessages", [])
            price_desc_parts = [msg.get("value", "") for msg in price_messages]
            price_description = " ".join(price_desc_parts).strip()

            # Image
            # image_url = hotel.get("propertyImage", {}).get("image", {}).get("url", "")

            # Reviews
            reviews = hotel.get("reviews", {})
            rating = reviews.get("score", "N/A")
            review_count = reviews.get("total", "N/A")

            # Final formatted hotel dict
            hotel_info = {
                "name": name,
                "stars": stars,
                "location": neighborhood,
                "region_id": region_id,
                "availability": availability_str,
                "price": display_price,
                "price_description": price_description,
                "rating": rating,
                "reviews_count": review_count,
                # "image": image_url
            }

            formatted_hotels.append(hotel_info)

        return formatted_hotels

    except Exception as e:
        return [{"error": f"Error formatting hotel data: {str(e)}"}]
