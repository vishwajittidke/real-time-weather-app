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
    

class errorhandling:
    cod : str


load_dotenv()
api_key = os.getenv('API_KEY') 

users_preferences = {
    'locations' : [],
    'units_in_metric' : 'metric',
    'units_in_imperial' : 'imperial'
}


def get_lat_lon(city_name, api_key):
    resp = requests.get(f'https://api.openweathermap.org/geo/1.0/direct?q={city_name}&appid={api_key}&units=metric').json()
    if resp and resp[0].get('lat') and resp[0].get('lon'):
        data = resp[0]
        lat, lon = data.get('lat'), data.get('lon') 
        
        return lat, lon
    else:
        raise ValueError(f"City '{city_name}' not found")



def get_current_weather(lat, lon, api_key):
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

def add_location(location):
    users_preferences['locations'].append(location)

def remove_location(location):
    users_preferences['locations'].remove(location)

def set_units(units):
    users_preferences['units'] = units

def get_user_preferences():
    return users_preferences

def main(city_name):
    try:
        lat, lon = get_lat_lon(city_name, api_key)
        weather_data = get_current_weather(lat, lon, api_key)
        return weather_data
    
    except ValueError as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    lat, lon = get_lat_lon('Akola', api_key)
    get_current_weather(lat, lon, api_key)
