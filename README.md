# 🌤 Weather App

A simple weather app built with **HTML, CSS, JavaScript** and **Python (Flask)**.

**Live Demo**: [bharath1461.github.io/Weather](https://bharath1461.github.io/Weather/)

## Features

- 🔍 Search any city worldwide
- 🌡 Current temperature, feels-like, humidity, wind speed
- 📅 5-day forecast
- 📱 Works on any device (phone, tablet, desktop)

## How It Works

The app calls [WeatherAPI.com](https://www.weatherapi.com/) to get weather data and displays it in a clean UI.

| File | Purpose |
|------|---------|
| `index.html` | Page structure |
| `style.css` | Styling and layout |
| `app.js` | Fetches weather data and updates the page |
| `app.py` | (Optional) Python server for running locally |

## Run Locally with Python

```bash
# 1. Install dependencies
python -m pip install flask requests python-dotenv

# 2. Add your API key
copy .env.example .env
# Edit .env and add your WeatherAPI.com key

# 3. Run
python app.py

# 4. Open http://localhost:5000
```

## API

Uses [WeatherAPI.com](https://www.weatherapi.com/) — free tier, sign up to get a key.
