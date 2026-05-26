# ==========================================
#  Weather App — Simple Python Flask Server
# ==========================================

# Step 1: Import the libraries we need
from flask import Flask, request, jsonify, send_from_directory
import requests

# Step 2: Create the Flask app
app = Flask(__name__)

# Step 3: Store our API key
API_KEY = "363554375c2240af960152946262605"


# Step 4: Home page — show index.html when user visits the site
@app.route("/")
def home():
    return send_from_directory(".", "index.html")


# Step 5: Weather API — get weather data for a city
@app.route("/api/weather")
def weather():
    # Get the city name from the URL (example: /api/weather?city=Mysore)
    city = request.args.get("city")

    # Call WeatherAPI.com to get the weather
    url = f"https://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={city}&days=5"
    response = requests.get(url)
    data = response.json()

    # If city not found, show error
    if "error" in data:
        return jsonify({"error": data["error"]["message"]}), 404

    # Send the weather data back to the frontend
    return jsonify(data)


# Step 6: Run the server
if __name__ == "__main__":
    app.run(debug=True, port=5000)
