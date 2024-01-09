from django.shortcuts import render, redirect
from django.contrib import messages
import requests
import datetime
from django.http import JsonResponse

# Initialize a dummy list of favorite cities
favorite_cities = []

def home(request):
    api_key = '21cacb89bb0c4863843161528240101'

    if 'city' in request.POST:
        city = request.POST['city']
    else:
        city = 'indore'

    url = f'http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}'
    PARAMS = {'units': 'metric'}

    try:
        data = requests.get(url, params=PARAMS).json()
        description = data['current']['condition']['text']
        icon = data['current']['condition']['icon']
        temp = data['current']['temp_c']
        humidity = data['current']['humidity']
        wind_speed = data['current']['wind_kph']
        day = datetime.date.today()
        city_name = data['location']['name']
    except Exception as e:
        # Handle the case when the API request fails
        messages.error(request, f"Error fetching data: {e}")
        description, icon, temp, humidity, wind_speed, day, city_name = "", "", "", "", "", "", ""

    return render(request, 'weatherapp/index.html', {
        'description': description,
        'icon': icon,
        'temp': temp,
        'humidity': humidity,
        'wind_speed': wind_speed,
        'day': day,
        'city_name': city_name,
        'favorite_cities': favorite_cities,
    })

def add_to_favorite(request, city):
    if city not in favorite_cities:
        favorite_cities.append(city)
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'message': f"{city} is already in the favorite list"})

def remove_from_favorite(request, city):
    if city in favorite_cities:
        favorite_cities.remove(city)
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'message': f"{city} is not in the favorite list"})

def refresh_weather(request):
    api_key = '21cacb89bb0c4863843161528240101'

    if 'city' in request.GET:
        city = request.GET['city']
    else:
        city = 'indore'

    url = f'http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}'
    PARAMS = {'units': 'metric'}

    try:
        data = requests.get(url, params=PARAMS).json()
        description = data['current']['condition']['text']
        icon = data['current']['condition']['icon']
        temp = data['current']['temp_c']
        humidity = data['current']['humidity']
        wind_speed = data['current']['wind_kph']
        day = datetime.date.today()
        city_name = data['location']['name']
    except Exception as e:
        return JsonResponse({'error': f"Error fetching data: {e}"}, status=500)

    weather_data = {
        'description': description,
        'icon': icon,
        'temp': temp,
        'humidity': humidity,
        'wind_speed': wind_speed,
        'day': day,
        'city_name': city_name,
        'favorite_cities': favorite_cities,
    }
    return JsonResponse(weather_data)
