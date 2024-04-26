from flask import Flask, request, jsonify, session, Blueprint, redirect, url_for, render_template, flash
import psycopg2
import psycopg2.extras
import re 

user_blueprint = Blueprint('user_blueprint',__name__)
user_blueprint.secret_key = 'hello'

app = Flask(__name__)


@user_blueprint.route('/api/login', methods=['POST'])
def login(username, password):
    username = request.json.get('username')
    password = request.json.get('password')
    # Verify username and password
    if username == 'admin' and password == 'admin':
        session['logged_in'] = True
        return jsonify({'message': 'Logged in successfully'})
    else:
        return jsonify({'message': 'Login failed'}), 401

