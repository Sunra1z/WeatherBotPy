import requests
import json

weather_emojis = { # Emojis for weather
    "clear sky": "☀️",
    "few clouds": "🌤️",
    "scattered clouds": "🌥️",
    "broken clouds": "🌥️",
    "shower rain": "🌦️",
    "rain": "🌧️",
    "thunderstorm": "⛈️",
    "snow": "❄️",
    "mist": "🌫️",
    "fog": "🌫️"
}

def weather_translate(data: dict) -> str: # Translate weather data to human-readable format
    city = data['name']
    temp = data['main']['temp']
    feels_like = data['main']['feels_like']
    weather_description = data['weather'][0]['description']
    emoji = weather_emojis.get(weather_description, '')

    if temp < 0:  # Freezing
        custom_message = "Brrr, it's freezing! Don't forget your gloves and hat! 🧤🧣"
    elif 0 <= temp < 10:  # Cold
        custom_message = "It's quite chilly, better wear a warm jacket! 🧥"
    elif 10 <= temp < 20:  # Mild
        custom_message = "The weather is mild, a light sweater should be enough. 🧶"
    elif 20 <= temp < 30:  # Warm
        custom_message = "It's warm outside, perfect for a t-shirt! 👕"
    elif temp >= 30:  # Hot
        custom_message = "It's really hot! Don't forget to stay hydrated! 🥤"

    return f"Weather in {city}:\n{weather_description} {emoji}\nTemperature: {temp:.2f}°C\nFeels like: {feels_like:.2f}°C\n{custom_message}"
def get_weather_data(city: str, api_token: str) -> dict: # Get weather data from OpenWeatherMap API
    """
    Get weather data from OpenWeatherMap API
    :param city: city name
    :param api_token: API token
    :return: weather data
    """
    try: # JSON Parsing
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_token}&units=metric"
        response = requests.get(url)
        data = json.loads(response.text)
        return data
    except Exception as e:
        print(e)
        return None