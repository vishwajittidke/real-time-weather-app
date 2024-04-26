from flask import Flask, request, jsonify, Blueprint

from backend.weather_api import main

my_blueprint = Blueprint('my_blueprint',__name__)

@my_blueprint.route('/weather', methods=['GET'])
def get_weather():
    city_name = request.args.get('city_name')
    weather_data = main(city_name)
    return jsonify(weather_data)
