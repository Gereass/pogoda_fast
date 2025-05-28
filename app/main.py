from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime
import requests

app = FastAPI()

aa= [{'time': '2025-05-28T00:00', 'temperature': 18.4, 'humidity': 0, 'wind_speed': 0}, 
     {'time': '2025-05-28T01:00', 'temperature': 17.8, 'humidity': 0, 'wind_speed': 0},
       {'time': '2025-05-28T02:00', 'temperature': 17.1, 'humidity': 0, 'wind_speed': 0},
         {'time': '2025-05-28T03:00', 'temperature': 15.6, 'humidity': 0, 'wind_speed': 0},
           {'time': '2025-05-28T04:00', 'temperature': 15.1, 'humidity': 0, 'wind_speed': 0}, 
           {'time': '2025-05-28T05:00', 'temperature': 14.6, 'humidity': 0, 'wind_speed': 0}, 
           {'time': '2025-05-28T06:00', 'temperature': 15.7, 'humidity': 0, 'wind_speed': 0}, 
           {'time': '2025-05-28T07:00', 'temperature': 17.0, 'humidity': 0, 'wind_speed': 0}, 
           {'time': '2025-05-28T08:00', 'temperature': 18.9, 'humidity': 0, 'wind_speed': 0}, 
           {'time': '2025-05-28T09:00', 'temperature': 21.1, 'humidity': 0, 'wind_speed': 0}, 
           {'time': '2025-05-28T10:00', 'temperature': 23.3, 'humidity': 0, 'wind_speed': 0}, 
           {'time': '2025-05-28T11:00', 'temperature': 25.2, 'humidity': 0, 'wind_speed': 0}, 
           {'time': '2025-05-28T12:00', 'temperature': 26.3, 'humidity': 0, 'wind_speed': 0}, 
           {'time': '2025-05-28T13:00', 'temperature': 26.9, 'humidity': 0, 'wind_speed': 0}, 
           {'time': '2025-05-28T14:00', 'temperature': 27.4, 'humidity': 0, 'wind_speed': 0}, 
           {'time': '2025-05-28T15:00', 'temperature': 27.7, 'humidity': 0, 'wind_speed': 0}, 
           {'time': '2025-05-28T16:00', 'temperature': 27.7, 'humidity': 0, 'wind_speed': 0}, 
           {'time': '2025-05-28T17:00', 'temperature': 27.5, 'humidity': 0, 'wind_speed': 0}, 
           {'time': '2025-05-28T18:00', 'temperature': 27.0, 'humidity': 0, 'wind_speed': 0}, 
           {'time': '2025-05-28T19:00', 'temperature': 26.2, 'humidity': 0, 'wind_speed': 0}, 
           {'time': '2025-05-28T20:00', 'temperature': 24.9, 'humidity': 0, 'wind_speed': 0}, 
           {'time': '2025-05-28T21:00', 'temperature': 23.0, 'humidity': 0, 'wind_speed': 0},
             {'time': '2025-05-28T22:00', 'temperature': 21.2, 'humidity': 0, 'wind_speed': 0},
               {'time': '2025-05-28T23:00', 'temperature': 20.0, 'humidity': 0, 'wind_speed': 0}]



# Настройка шаблонизатора Jinja2
templates = Jinja2Templates(directory="app/templates")

# Функция для получения координат города через Open-Meteo Geocoding
def get_coordinates(city_name: str):
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {
        "name": city_name,
        "count": 1  # Возвращаем только первое совпадение
    }
    response = requests.get(url, params=params).json()
    if "results" in response:
        result = response["results"][0]
        return float(result["latitude"]), float(result["longitude"])
    return None, None

def process_data(response: list):
     # Извлечение данных из ответа
    # hourly_data = response.get("hourly", {})
    # times = hourly_data.get("time", [])
    # temperatures = hourly_data.get("temperature_2m", [])
    # humidity = hourly_data.get("relative_humidity_2m", [])
    # wind_speed = hourly_data.get("wind_speed_10m", [])

    # Формирование удобного вывода
    # forecast = []
    # for i in range(len(times)):  # Берём первые 5 временных меток
    #     forecast.append({
    #         "time": times[i],
    #         "temperature": temperatures[i],
    #         "humidity": 0, #humidity[i],
    #         "wind_speed": 0, # wind_speed[i]
    #     })

    current_time = datetime.now().strftime("%Y-%m-%dT%H:00")
    current_weather = next((item for item in aa if item["time"] == current_time), None)

    forecast = response
    print(current_weather)

    return current_weather

# Главная страница
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Обработка POST-запроса для получения прогноза погоды
@app.post("/weather/", response_class=HTMLResponse)
async def get_weather(request: Request, city: str = Form(...)):
    # latitude, longitude = get_coordinates(city)
    # if not latitude or not longitude:
    #     return templates.TemplateResponse(
    #         "index.html",
    #         {"request": request, "error": "Город не найден. Попробуйте снова."}
    #     )
    # # Запрос к Open-Meteo API
    # url = "https://api.open-meteo.com/v1/forecast"
    # params = {
    #     "latitude": latitude,
    #     "longitude": longitude,
    #     "hourly": "temperature_2m",
    #     "current": "temperature_2m",
    #     "forecast_days": 1,
    #     "timezone": "Europe/Moscow",
    #     "current_weather": True,
    # }
    # response = requests.get(url, params=params).json()

    # forecast= process_data(response)
    forecast= process_data(aa)
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "city": city, "forecast": forecast}
    )