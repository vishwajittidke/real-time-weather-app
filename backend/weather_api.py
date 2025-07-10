import requests
from dotenv import load_dotenv
import os
from dataclasses import dataclass

@dataclass
class WeatherData:
    main : str 
    description : str
    icon : str
    temperature : float
    feelsLike : float
    tempMin : float
    tempMax : float
    humidity : float
    windSpeed : float
    windDeg : str
    cityName : str
    


load_dotenv()
api_key = os.getenv('API_KEY') 
print(f"[DEBUG] Loaded API Key: {api_key}")


def get_lat_lon(city_name, api_key):
    try:
        print(f"[DEBUG] Fetching coordinates for city: {city_name}")
        resp = requests.get(
            f'https://api.openweathermap.org/geo/1.0/direct?q={city_name}&appid={api_key}&units=metric'
        )
        if resp.status_code != 200:
            print(f"[ERROR] API returned {resp.status_code}: {resp.text}")
            return None, None
        
        data = resp.json()
        if not data or 'lat' not in data[0] or 'lon' not in data[0]:
            print(f"[ERROR] City not found in response data: {data}")
            return None, None

        lat = data[0]['lat']
        lon = data[0]['lon']
        print(f"[DEBUG] Found coordinates: lat={lat}, lon={lon}")
        return lat, lon

    except Exception as e:
        print(f"[EXCEPTION] Unexpected error in get_lat_lon: {type(e).__name__}: {str(e)}")
        return None, None


def get_current_weather(lat, lon, api_key):
        
    try:
        resp = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric').json()
        
        data = WeatherData (
            main=resp.get('weather')[0].get('main'),
            description=resp.get('weather')[0].get('description'),
            icon=resp.get('weather')[0].get('icon'),
            temperature=resp.get('main').get('temp'),
            feelsLike=resp.get('main').get('feels_like'),
            tempMin=resp.get('main').get("temp_min"),
            tempMax=resp.get('main').get( "temp_max"),
            humidity=resp.get('main').get('humidity'),
            windSpeed = resp.get('wind').get('speed'),
            windDeg = resp.get('wind').get('deg'),
            cityName= resp.get('name')

        )
        return data
    
    except Exception as e:
        print(f"[EXCEPTION] Failed to fetch weather: {type(e).__name__}: {str(e)}")
        return None


def main(city_name):
    lat, lon = get_lat_lon(city_name, api_key)
    if not lat or not lon:
        print(f"City Not found")
        return None

    weather_data = get_current_weather(lat, lon, api_key)
    if not weather_data:
        print(f"Enter correct city name")
        return None

    return weather_data

if __name__ == "__main__":
    lat, lon = get_lat_lon('Akola', api_key)
    get_current_weather(lat, lon, api_key)
