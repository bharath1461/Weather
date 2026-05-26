"""
Weather App — Python Flask Backend (for local use)
===================================================
This file runs a local web server using Flask.
It fetches weather data from WeatherAPI.com and sends it to the frontend.

Note: For GitHub Pages deployment, the static files (index.html, style.css, app.js)
      call the API directly from the browser. This Python file is only needed
      if you want to run the app locally with Python.

How to run:
    1. Install dependencies:  python -m pip install flask requests python-dotenv
    2. Create a .env file:    WEATHER_API_KEY=your_key_here
    3. Run:                   python app.py
    4. Open:                  http://localhost:5000
"""

# --- Import libraries ---
import os                          # For reading environment variables
from flask import Flask, request, jsonify, send_from_directory
import requests                    # For making HTTP requests to the weather API
from dotenv import load_dotenv     # For loading .env file

# Load environment variables from .env file
load_dotenv()

# --- Create the Flask app ---
app = Flask(__name__, static_folder=".", static_url_path="")

# Read the API key from the .env file
API_KEY = os.getenv("WEATHER_API_KEY")

# WeatherAPI.com endpoint — gives current weather + forecast in one call
API_URL = "https://api.weatherapi.com/v1/forecast.json"


# --- Route: Home page ---
# When someone visits http://localhost:5000/, serve index.html
@app.route("/")
def home():
    return send_from_directory(".", "index.html")


# --- Route: Weather API ---
# When the frontend asks for weather data, fetch it from WeatherAPI.com
@app.route("/api/weather")
def get_weather():
    # Get the city name from the URL (e.g., /api/weather?city=Mysore)
    city = request.args.get("city", "").strip()

    # If no city was provided, return an error
    if not city:
        return jsonify({"error": "Please enter a city name."}), 400

    # If the API key is missing, return an error
    if not API_KEY or API_KEY == "your_api_key_here":
        return jsonify({"error": "API key not set. Add it to .env file."}), 500

    try:
        # Build the request parameters
        params = {
            "key": API_KEY,    # API key for authentication
            "q": city,         # City name to search
            "days": 5,         # Number of forecast days
            "aqi": "no",       # We don't need air quality data
        }

        # Make the API request to WeatherAPI.com
        response = requests.get(API_URL, params=params, timeout=10)
        data = response.json()

        # If the API returned an error, pass it to the frontend
        if "error" in data:
            return jsonify({"error": data["error"]["message"]}), 404

        # Extract the data we need from the API response
        current = data["current"]
        location = data["location"]
        forecast_days = data["forecast"]["forecastday"]

        # Build a clean response for the frontend
        result = {
            "city": location["name"],
            "country": location["country"],
            "temp": round(current["temp_c"]),
            "feels_like": round(current["feelslike_c"]),
            "humidity": current["humidity"],
            "wind_speed": round(current["wind_kph"], 1),
            "description": current["condition"]["text"],
            "icon": current["condition"]["icon"],
            "forecast": [
                {
                    "date": day["date"],
                    "temp": round(day["day"]["avgtemp_c"]),
                    "icon": day["day"]["condition"]["icon"],
                    "description": day["day"]["condition"]["text"],
                }
                for day in forecast_days
            ],
        }

        # Send the weather data back as JSON
        return jsonify(result)

    # Handle network errors
    except requests.exceptions.ConnectionError:
        return jsonify({"error": "No internet connection."}), 503
    except requests.exceptions.Timeout:
        return jsonify({"error": "Request timed out. Try again."}), 504
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500


# --- Start the server ---
# This only runs when you execute: python app.py
if __name__ == "__main__":
    print("Weather app running at http://localhost:5000")
    app.run(debug=True, port=5000)
