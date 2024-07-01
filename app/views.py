from django.shortcuts import render

# Create your views here.
import requests
from django.http import JsonResponse

def stageone(request):
    visitor_name = request.GET.get('visitor_name', 'Guest')

    # Get client IP
    client_ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR'))

    try:
        # Get location info
        location_response = requests.get(f'http://ipinfo.io/{client_ip}/json')
        location_data = location_response.json()
        city = location_data.get('city', 'Unknown City')

        if city == 'Unknown City':
            raise ValueError('City could not be determined from IP address')

        # Get weather info
        weather_response = requests.get(
            f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid=5d283a99d22ce2b152ec51514eb42a88'
        )
        weather_data = weather_response.json()

        if 'main' not in weather_data:
            raise ValueError(f"Weather data not found for city: {city}. Response: {weather_data}")

        temperature = weather_data['main']['temp']

        response = {
            "client_ip": client_ip,
            "location": city,
            "greeting": f"Hello, {visitor_name}!, the temperature is {temperature} degrees Celsius in {city}"
        }
    except Exception as e:
        response = {"error": str(e)}

    return JsonResponse(response)
