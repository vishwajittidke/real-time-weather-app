from flask import Flask
from flask_socketio import SocketIO
from dotenv import load_dotenv
import requests
import os
from dataclasses import dataclass

@dataclass
class WeatherData:
    main : str 
    description : str
    icon : str
    temperature : float
    humidity : float


app = Flask(__name__)
socketio = SocketIO(app)

load_dotenv()
api_key = os.getenv('API_KEY') 


def get_weather_data(city_name, api_key):
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric'
    response = requests.get(url)
    data = response.json()
    return data

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    # Get weather data for a specific location (e.g., Akola)
    weather_data = get_weather_data('Akola')
    data = WeatherData (
            main=weather_data.get('weather')[0].get('main'),
            description=weather_data.get('weather')[0].get('description'),
            icon=weather_data.get('weather')[0].get('icon'),
            temperature=weather_data.get('main').get('temp'),
            humidity=weather_data.get('main').get('humidity')

        )
        
    return data

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app, debug=True)
    print(get_weather_data('Akola', api_key))
