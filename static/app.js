// Weather App — Client

const form    = document.getElementById("search-form");
const input   = document.getElementById("city-input");
const errorEl = document.getElementById("error");
const loader  = document.getElementById("loader");
const weather = document.getElementById("weather");

const DAYS = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];

function showError(msg) {
    errorEl.textContent = msg;
    errorEl.classList.add("visible");
}

function hideError() {
    errorEl.classList.remove("visible");
}

function setLoading(on) {
    loader.classList.toggle("visible", on);
    if (on) {
        weather.classList.remove("visible");
        hideError();
    }
}

function fixIcon(url) {
    // WeatherAPI returns protocol-relative URLs like //cdn.weatherapi.com/...
    if (url && url.startsWith("//")) return "https:" + url;
    return url;
}

function dayName(dateStr) {
    return DAYS[new Date(dateStr + "T12:00:00").getDay()];
}

function render(d) {
    document.getElementById("w-city").textContent  = `${d.city}, ${d.country}`;
    document.getElementById("w-desc").textContent  = d.description;
    document.getElementById("w-temp").textContent  = `${d.temp}°`;
    document.getElementById("w-feels").textContent = `${d.feels_like}°`;
    document.getElementById("w-humidity").textContent = `${d.humidity}%`;
    document.getElementById("w-wind").textContent  = `${d.wind_speed} km/h`;

    const icon = document.getElementById("w-icon");
    icon.src = fixIcon(d.icon);
    icon.alt = d.description;

    const fc = document.getElementById("forecast");
    fc.innerHTML = d.forecast.map(f => `
        <div class="fc">
            <div class="fc-day">${dayName(f.date)}</div>
            <img src="${fixIcon(f.icon)}" alt="${f.description}" width="36" height="36">
            <div class="fc-temp">${f.temp}°</div>
        </div>
    `).join("");

    weather.classList.add("visible");
}

async function fetchWeather(city) {
    setLoading(true);
    try {
        const res  = await fetch(`/api/weather?city=${encodeURIComponent(city)}`);
        const data = await res.json();
        setLoading(false);

        if (!res.ok) {
            showError(data.error || "Something went wrong.");
            return;
        }
        render(data);
    } catch {
        setLoading(false);
        showError("Network error. Check your connection.");
    }
}

form.addEventListener("submit", e => {
    e.preventDefault();
    const city = input.value.trim();
    if (city) fetchWeather(city);
});
