# 🌤 Weather App

A minimal, beautiful weather app built with **Python + Flask** and a glassmorphism dark UI.

## Features

- 🔍 Search any city worldwide
- 🌡 Current temperature, feels-like, humidity, wind, pressure, visibility
- 📅 5-day forecast with icons
- ✨ Glassmorphism dark theme with ambient animations

## Setup

### 1. Get an API key

Sign up at [OpenWeatherMap](https://openweathermap.org/api) (free tier works) and copy your API key.

### 2. Configure

```bash
copy .env.example .env
```

Edit `.env` and replace `your_api_key_here` with your actual key.

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Run

```bash
python app.py
```

Open [http://localhost:5000](http://localhost:5000) in your browser.

## Tech Stack

| Layer    | Technology          |
|----------|---------------------|
| Backend  | Python, Flask       |
| Frontend | HTML, CSS, JS       |
| API      | OpenWeatherMap      |
| Design   | Glassmorphism, Dark |
