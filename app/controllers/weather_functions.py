import requests
import os
from datetime import datetime
from dotenv import load_dotenv

# Load the .env file
load_dotenv()
api_key = os.getenv("WEATHER_API_KEY")
# Replace with your OpenWeatherMap API key


# Specify the city and optionally the country code (e.g., London,uk)
location = "Cleveland"
# Specify the particular date (format: YYYY-MM-DD)
selected_date = "2023-10-06"


def check_the_date(dateStr):
    # Given date in 'YYYY-MM-DD' format
    given_date = datetime.strptime(dateStr, "%Y-%m-%d").date()
    # Get today's date
    current_date = datetime.now().date()
    # Compare the given date with today's date
    if given_date < current_date:
        return "history"
    elif given_date == current_date:
        return "current"
    else:
        return "forecast"


# Make a request to the WeatherAPI for the forecast


def specific_date_weather(specific_date):
    url = f"http://api.weatherapi.com/v1/{check_the_date(specific_date)}.json?key={api_key}&q={location}&dt={specific_date}"
    print(url)
    # Fetch the weather details for the particular date
    response = requests.get(url)
    data = response.json()

    # Print the weather details
    if response.status_code == 200:
        max_temp = data["forecast"]["forecastday"][0]["day"]["maxtemp_c"]
        min_temp = data["forecast"]["forecastday"][0]["day"]["mintemp_c"]
        condition = data["forecast"]["forecastday"][0]["day"]["condition"]["text"]
        print(f"On {specific_date}, in {location}:")
        print(f"Max Temperature: {max_temp}°C")
        print(f"Min Temperature: {min_temp}°C")
        print(f"Condition: {condition}")
    else:
        print(f"Failed to retrieve data: {data}")


def weather_for_one_week():
    url = (
        f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={location}&days=7"
    )
    # Fetch the weather forecast
    response = requests.get(url)
    data = response.json()
    # Print the weather forecast for the next week and for the specific date
    if response.status_code == 200:
        # Print forecast for each day in the next week
        for forecast in data["forecast"]["forecastday"]:
            date = forecast["date"]
            condition = forecast["day"]["condition"]["text"]
            max_temp = forecast["day"]["maxtemp_c"]
            min_temp = forecast["day"]["mintemp_c"]
            print(
                f"On {date}, the weather in {location} is expected to be {condition.lower()} with a high of {max_temp}°C and a low of {min_temp}°C."
            )
    else:
        print(f"Failed to retrieve data: {data}")


# weather_for_one_week()
specific_date_weather(selected_date)
