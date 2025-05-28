from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from datetime import datetime
import requests


app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Функция для получения координат города через Open-Meteo Geocoding
def get_coordinates(city_name: str):
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {
        "name": city_name,
        "count": 1 
    }
    response = requests.get(url, params=params).json()
    if "results" in response:
        result = response["results"][0]
        return float(result["latitude"]), float(result["longitude"])
    return None, None

# Функция для обработки данных ответа
def process_data(response: list):
    hourly_data = response.get("hourly", {})
    times = hourly_data.get("time", [])
    temperatures = hourly_data.get("temperature_2m", [])

    forecast = []
    for i in range(len(times)):
        forecast.append({
            "time": times[i],
            "temperature": temperatures[i],
        })

    current_time = datetime.now().strftime("%Y-%m-%dT%H:00")
    forecast_now = next((item for item in forecast if item["time"] == current_time), None)

    return forecast, forecast_now


# Главная страница
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Обработка POST-запроса для получения прогноза погоды
@app.post("/weather/", response_class=HTMLResponse)
async def get_weather(request: Request, city: str = Form(...)):
    latitude, longitude = get_coordinates(city)
    if not latitude or not longitude:
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "error": "Город не найден. Попробуйте снова."}
        )
    
    # Запрос к Open-Meteo API
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "temperature_2m",
        "current": "temperature_2m",
        "forecast_days": 1,
        "timezone": "Europe/Moscow",
        "current_weather": True,
    }

    response = requests.get(url, params=params).json()
    forecast, forecast_now= process_data(response)

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "city": city, "forecast": forecast, "forecast_now": forecast_now,}
    )
