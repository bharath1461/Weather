import os
from flask import Flask, render_template, request, jsonify
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("WEATHER_API_KEY")
FORECAST_URL = "https://api.weatherapi.com/v1/forecast.json"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/weather")
def get_weather():
    city = request.args.get("city", "").strip()
    if not city:
        return jsonify({"error": "Please enter a city name."}), 400

    if not API_KEY or API_KEY == "your_api_key_here":
        return jsonify({"error": "API key not configured. Add your WeatherAPI key to .env"}), 500

    try:
        params = {"key": API_KEY, "q": city, "days": 5, "aqi": "no"}
        resp = requests.get(FORECAST_URL, params=params, timeout=10)
        data = resp.json()

        # WeatherAPI returns error object on failure
        if "error" in data:
            msg = data["error"].get("message", "Something went wrong.")
            code = data["error"].get("code", 0)
            status = 404 if code == 1006 else 400
            return jsonify({"error": msg}), status

        current = data["current"]
        location = data["location"]
        forecast_days = data["forecast"]["forecastday"]

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
                for day in forecast_days[:5]
            ],
        }
        return jsonify(result)

    except requests.exceptions.ConnectionError:
        return jsonify({"error": "No internet connection."}), 503
    except requests.exceptions.Timeout:
        return jsonify({"error": "Request timed out. Try again."}), 504
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
