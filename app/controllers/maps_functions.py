import requests
import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()
subscription_key = os.getenv("AZURE_MAPS_API_KEY")


# Convert place names to coordinates using the Search Service
def get_coordinates(place_name):
    url = f"https://atlas.microsoft.com/search/fuzzy/json?subscription-key={subscription_key}&api-version=1.0&query={place_name}"
    response = requests.get(url)
    if response.status_code == 200:
        coordinates = response.json()["results"][0]["position"]
        return f'{coordinates["lat"]},{coordinates["lon"]}'
    else:
        print(f"Failed to get coordinates for {place_name}")
        return None


# Get route directions using coordinates with the Route Service
def get_route_directions(start_place, end_place):
    start_coordinates = get_coordinates(start_place)
    end_coordinates = get_coordinates(end_place)
    print(start_coordinates, end_coordinates)
    # Create the URL for the API request
    url = f"https://atlas.microsoft.com/route/directions/json?subscription-key={subscription_key}&api-version=1.0&query={start_coordinates}:{end_coordinates}"

    # Make a GET request to fetch the route data
    response = requests.get(url)
    data = response.json()
    # print(data)
    # Print the route instructions if the request was successful
    if response.status_code == 200:
        route = response.json()["routes"][0]["legs"][0]["summary"]
        print(f"Distance: {route['lengthInMeters'] * 0.001:.2f} km")
        travel_time_in_minutes = route["travelTimeInSeconds"] / 60
        # Convert travel time to hours if it is more than 120 minutes
        if travel_time_in_minutes > 120:
            print(f"Travel Time: {travel_time_in_minutes / 60:.2f} hours")
        else:
            print(f"Travel Time: {travel_time_in_minutes:.2f} minutes")
    else:
        print("Failed to retrieve the route directions.")


# Example usage
start_place = "New York, NY"
end_place = "Los Angeles, CA"
get_route_directions(start_place, end_place)
