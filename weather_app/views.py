from django.shortcuts import render
import requests
from datetime import datetime
import pytz

def get_weather(city):
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    api_key = "4fcd66a437ba7800273eea9ccc745721"  # Replace with your actual API key
    parameters = {
        'q': city,
        'appid': api_key,
        'units': 'metric'
    }
    response = requests.get(base_url, params=parameters)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_local_time(timezone_str):
    try:
        tz = pytz.timezone(timezone_str)
        return datetime.now(tz).strftime("%d, %B - %I:%M %p")
    except pytz.UnknownTimeZoneError:
        return "Unknown Time Zone"

def home(request):
    city = request.GET.get('city')
    icon_url = 'https://openweathermap.org/img/wn/10d@2x.png'
    weather = weather_description = country = None
    wind_speed = pressure = humidity = temperature = cloudiness = None
    current_time = ""

    if city:
        weather_data_result = get_weather(city)

        if weather_data_result is not None:
            icon_id = weather_data_result['weather'][0]['icon']
            icon_url = f"https://openweathermap.org/img/wn/{icon_id}@2x.png"
            weather = weather_data_result['weather'][0]['main']
            weather_description = weather_data_result['weather'][0]['description']
            city = weather_data_result['name']
            country = weather_data_result['sys']['country']
            wind_speed = weather_data_result['wind']['speed']
            pressure = weather_data_result['main']['pressure']
            humidity = weather_data_result['main']['humidity']
            temperature = weather_data_result['main']['temp']
            cloudiness = weather_data_result['clouds']['all']  # Cloudiness percentage
            timezone_offset = weather_data_result['timezone']
            
            # Convert timezone offset to timezone name
            timezone_str = pytz.country_timezones.get(country, [None])[0]
            if timezone_str:
                current_time = get_local_time(timezone_str)
            else:
                current_time = "Unknown Time Zone"

    context = {
        'icon_url': icon_url,
        'weather': weather,
        'weather_description': weather_description,
        'city': city,
        'country': country,
        'wind_speed': wind_speed,
        'pressure': pressure,
        'humidity': humidity,
        'temperature': temperature,
        'cloudiness': cloudiness,
        'current_time': current_time
    }

    return render(request, 'index.html', context)
