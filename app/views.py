import os
import requests
from django.http import JsonResponse

def hello(request, visitor_name):
    provided_city = request.GET.get('city')
    api_key = os.getenv('OPENWEATHERMAP_API_KEY')

    # Get client IP
    client_ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR'))

    try:
        if provided_city:
            city = provided_city
        else:
            # Get location info based on IP
            location_response = requests.get(f'http://ipinfo.io/{client_ip}/json')
            location_data = location_response.json()
            city = location_data.get('city', 'Unknown City')

        if city == 'Unknown City':
            raise ValueError('City could not be determined from IP address')

        # Get weather info
        weather_response = requests.get(
            f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}'
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
