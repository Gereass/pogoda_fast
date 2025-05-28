import pytest
import requests
from app.main import get_coordinates, process_data

MOCK_CITY = "Moscow"
MOCK_LATITUDE = 55.7522
MOCK_LONGITUDE = 37.6156

FORECAST = [{'time': '2025-05-28T00:00', 'temperature': 18.0}, {'time': '2025-05-28T01:00', 'temperature': 17.6}, {'time': '2025-05-28T02:00', 'temperature': 17.5}, {'time': '2025-05-28T03:00', 'temperature': 16.3}, {'time': '2025-05-28T04:00', 'temperature': 16.7}, {'time': '2025-05-28T05:00', 'temperature': 18.6}, {'time': '2025-05-28T06:00', 'temperature': 20.4}, {'time': '2025-05-28T07:00', 'temperature': 22.4}, {'time': '2025-05-28T08:00', 'temperature': 24.5}, {'time': '2025-05-28T09:00', 'temperature': 26.8}, {'time': '2025-05-28T10:00', 'temperature': 28.2}, {'time': '2025-05-28T11:00', 'temperature': 29.4}, {'time': '2025-05-28T12:00', 'temperature': 30.0}, {'time': '2025-05-28T13:00', 'temperature': 30.1}, {'time': '2025-05-28T14:00', 'temperature': 29.9}, {'time': '2025-05-28T15:00', 'temperature': 29.4}, {'time': '2025-05-28T16:00', 'temperature': 28.4}, {'time': '2025-05-28T17:00', 'temperature': 26.4}, {'time': '2025-05-28T18:00', 'temperature': 24.3}, {'time': '2025-05-28T19:00', 'temperature': 21.6}, {'time': '2025-05-28T20:00', 'temperature': 20.8}, {'time': '2025-05-28T21:00', 'temperature': 20.3}, {'time': '2025-05-28T22:00', 'temperature': 19.5}, {'time': '2025-05-28T23:00', 'temperature': 18.7}]
FORECAST_NOW= {'time': '2025-05-28T15:00', 'temperature': 29.4}
RESPONSE = {'latitude': 37.5, 'longitude': 69.5, 'generationtime_ms': 0.3954172134399414, 'utc_offset_seconds': 10800, 'timezone': 'Europe/Moscow', 'timezone_abbreviation': 'GMT+3', 'elevation': 485.0, 'current_weather_units': {'time': 'iso8601', 'interval': 'seconds', 'temperature': '°C', 'windspeed': 'km/h', 'winddirection': '°', 'is_day': '', 'weathercode': 'wmo code'}, 'current_weather': {'time': '2025-05-28T15:45', 'interval': 900, 'temperature': 28.6, 'windspeed': 4.6, 'winddirection': 342, 'is_day': 1, 'weathercode': 1}, 'hourly_units': {'time': 'iso8601', 'temperature_2m': '°C'}, 'hourly': {'time': [...], 'temperature_2m': [...]}}


def test_get_coordinates():
    latitude, longitude, city_name = get_coordinates(MOCK_CITY)

    assert latitude is not None
    assert longitude is not None
    assert city_name is not None

    assert round(latitude, 2) == round(MOCK_LATITUDE, 2)
    assert round(longitude, 2) == round(MOCK_LONGITUDE, 2)


def test_invalid_city():
    latitude, longitude, city_name = get_coordinates("InvalidCityName")
    assert latitude is None
    assert longitude is None
    assert city_name is None

# def test_process_data():
#     forecast, forecast_now = process_data(RESPONSE)
    
#     assert forecast is not None
#     assert forecast_now is not None
    
#     assert forecast_now == FORECAST_NOW
#     assert forecast == FORECAST

    # forecast_now['time']
    # forecast_now['temperature']
