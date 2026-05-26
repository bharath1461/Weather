// =============================================
//  Weather App — Frontend JavaScript
//  Calls WeatherAPI.com directly from the browser
// =============================================

// --- API Key ---
// WeatherAPI.com free tier key
const API_KEY = "363554375c2240af960152946262605";
const API_URL = "https://api.weatherapi.com/v1/forecast.json";

// --- Get HTML elements ---
const form    = document.getElementById("search-form");
const input   = document.getElementById("city-input");
const errorEl = document.getElementById("error");
const loader  = document.getElementById("loader");
const weather = document.getElementById("weather");

// Day name abbreviations for the forecast
const DAYS = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];

// --- Helper functions ---

// Show an error message to the user
function showError(msg) {
    errorEl.textContent = msg;
    errorEl.classList.add("visible");
}

// Hide the error message
function hideError() {
    errorEl.classList.remove("visible");
}

// Show or hide the loading spinner
function setLoading(on) {
    loader.classList.toggle("visible", on);
    if (on) {
        weather.classList.remove("visible");
        hideError();
    }
}

// WeatherAPI returns icon URLs starting with "//" — add "https:"
function fixIcon(url) {
    if (url && url.startsWith("//")) return "https:" + url;
    return url;
}

// Convert a date string like "2026-05-27" to a day name like "Wed"
function dayName(dateStr) {
    return DAYS[new Date(dateStr + "T12:00:00").getDay()];
}

// --- Display weather data on the page ---
function render(data) {
    // Current weather
    const current  = data.current;
    const location = data.location;

    document.getElementById("w-city").textContent  = `${location.name}, ${location.country}`;
    document.getElementById("w-desc").textContent  = current.condition.text;
    document.getElementById("w-temp").textContent  = `${Math.round(current.temp_c)}°`;
    document.getElementById("w-feels").textContent = `${Math.round(current.feelslike_c)}°`;
    document.getElementById("w-humidity").textContent = `${current.humidity}%`;
    document.getElementById("w-wind").textContent  = `${Math.round(current.wind_kph)} km/h`;

    const icon = document.getElementById("w-icon");
    icon.src = fixIcon(current.condition.icon);
    icon.alt = current.condition.text;

    // 5-day forecast
    const forecastDays = data.forecast.forecastday;
    const fc = document.getElementById("forecast");
    fc.innerHTML = forecastDays.map(day => `
        <div class="fc">
            <div class="fc-day">${dayName(day.date)}</div>
            <img src="${fixIcon(day.day.condition.icon)}" alt="${day.day.condition.text}" width="36" height="36">
            <div class="fc-temp">${Math.round(day.day.avgtemp_c)}°</div>
        </div>
    `).join("");

    // Show the weather section
    weather.classList.add("visible");
}

// --- Fetch weather from WeatherAPI.com ---
async function fetchWeather(city) {
    setLoading(true);

    try {
        // Build the API URL with query parameters
        const url = `${API_URL}?key=${API_KEY}&q=${encodeURIComponent(city)}&days=5&aqi=no`;

        // Make the API request
        const res  = await fetch(url);
        const data = await res.json();

        setLoading(false);

        // Check if API returned an error
        if (data.error) {
            showError(data.error.message);
            return;
        }

        // Display the weather data
        render(data);

    } catch {
        setLoading(false);
        showError("Network error. Check your connection.");
    }
}

// --- Event: form submit ---
form.addEventListener("submit", (e) => {
    e.preventDefault();                    // Stop page from reloading
    const city = input.value.trim();       // Get the city name
    if (city) fetchWeather(city);          // Fetch weather if not empty
});
