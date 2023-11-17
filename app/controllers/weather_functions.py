import sqlite3
import os
import requests
from datetime import datetime, timedelta

import json
from dotenv import load_dotenv

# Load the .env file
load_dotenv()
api_key = os.getenv("WEATHER_API_KEY")
# Replace with your OpenWeatherMap API key


def setup_database():
    conn = sqlite3.connect("weather_cache.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS weather_cache (
            date TEXT,
            location TEXT,
            data TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (date, location)
        )
    """
    )
    conn.commit()
    conn.close()


setup_database()


def get_cached_weather(date, location):
    conn = sqlite3.connect("weather_cache.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT data FROM weather_cache WHERE date = ? AND location = ?",
        (date, location),
    )
    result = cursor.fetchone()
    conn.close()
    return json.loads(result[0]) if result else None


def cache_weather(date, location, data):
    conn = sqlite3.connect("weather_cache.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR REPLACE INTO weather_cache (date, location, data) VALUES (?, ?, ?)",
        (date, location, json.dumps(data)),
    )
    conn.commit()
    conn.close()


def check_weather_type(dateStr):
    given_date = datetime.strptime(dateStr, "%Y-%m-%d").date()
    current_date = datetime.now().date()
    # print({"given_date": given_date, "current_date": current_date})
    if given_date == current_date:
        return "current"
    if given_date < current_date:
        return "history"
    else:
        return "forecast"


def weather_for_one_week(location):
    current_date_str = datetime.now().strftime("%Y-%m-%d")
    for i in range(7):
        specific_date = (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d")
        specific_date_weather(specific_date, location)
        print("============================================================")


def specific_date_weather(specific_date, location):
    weather_type = check_weather_type(specific_date)
    endpoint = (
        "current"
        if weather_type == "current"
        else "forecast"
        if weather_type == "forecast"
        else "history"
    )
    cached_weather = get_cached_weather(specific_date, location)
    if cached_weather:
        print(f"Using cached data for {specific_date} in {location}")
        data = cached_weather
    else:
        url = f"http://api.weatherapi.com/v1/{endpoint}.json?key={api_key}&q={location}"
        if weather_type != "current":
            url += f"&dt={specific_date}"

        response = requests.get(url)
        data = response.json()
        if response.status_code == 200:
            cache_weather(specific_date, location, data)
        else:
            print(f"Failed to retrieve data: {data}")
            return

    # Print the weather details
    if weather_type == "current":
        print_current_weather(data, location)
    else:
        print_forecast_or_history_weather(data, specific_date, location, weather_type)


def print_current_weather(data, location):
    current_temp = data["current"]["temp_c"]
    condition = data["current"]["condition"]["text"]
    print(f"Current weather in {location}:")
    print(f"Temperature: {current_temp}°C")
    print(f"Condition: {condition}")


def print_forecast_or_history_weather(data, specific_date, location, weather_type):
    if "forecast" in data:
        weather_data = data["forecast"]["forecastday"][0]
        max_temp = weather_data["day"]["maxtemp_c"]
        min_temp = weather_data["day"]["mintemp_c"]
        condition = weather_data["day"]["condition"]["text"]
        weather_desc = "forecast" if weather_type == "forecast" else "historical"
        print(f"On {specific_date}, the {weather_desc} weather in {location} was:")
        print(f"Max Temperature: {max_temp}°C")
        print(f"Min Temperature: {min_temp}°C")
        print(f"Condition: {condition}")
    else:
        print(f"No {weather_type} data available for {specific_date} in {location}")


location = "Cleveland"
weather_for_one_week(location)

# specific_date_weather("2023-11-18", location)
