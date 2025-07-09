# from flask import Flask, flash, render_template, request, session, redirect, url_for
# import psycopg2
# import psycopg2.extras
# import re 
# import app
# import os


# from backend.websocket import socketio
# from backend.weather_api import main as get_weather

# DATABASE_URL = os.environ.get("DATABASE_URL")
# if not DATABASE_URL:
#     raise Exception("DATABASE_URL environment variable not set!")

# app = Flask(__name__, template_folder='static')
# app.secret_key = 'hello'


# # DB_HOST = "localhost"
# # DB_NAME = "weather_db"
# # DB_USER = "postgres"
# # DB_PASS = "postgres"
 
# conn = psycopg2.connect(DATABASE_URL)


# app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 



# socketio.init_app(app)


# @app.route('/')
# def home():
   
#     if 'loggedin' in session:
#         return render_template('index.html', username=session['username'])
#     return redirect(url_for('login'))  


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   
#     if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
#         username = request.form['username']
#         password = request.form['password']
#         print(password)
 
#         cursor.execute('SELECT * FROM user_details WHERE username = %s', (username,))
#         account = cursor.fetchone()
 
#         if account:
#             password_rs = account['password']
#             print(password_rs)
#             if request.method == "POST":
#                 session['loggedin'] = True
#                 session['id'] = account['id']
#                 session['username'] = account['username']
#                 return redirect(url_for('dashboard'))
#             else:
#                 flash('Incorrect username/password')
#         else:
#             flash('Incorrect username/password')
    
#     return render_template('login.html')

# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
 
#     if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
#         fullname = request.form['fullname']
#         username = request.form['username']
#         password = request.form['password']
#         email = request.form['email']
    
#         cursor.execute('SELECT * FROM user_details WHERE username = %s', (username,))
#         account = cursor.fetchone()
#         print(account)

#         if account:
#             flash('Account already exists!')
#         elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
#             flash('Invalid email address!')
#         elif not re.match(r'[A-Za-z0-9]+', username):
#             flash('Username must contain only characters and numbers!')
#         elif not username or not password or not email:
#             flash('Please fill out the form!')
#         else:
#             cursor.execute("INSERT INTO user_details (username, password, fullname, email) VALUES (%s,%s,%s,%s)", (username, password, fullname, email))
#             conn.commit()
#             flash('You have successfully registered!')
#             return render_template('login.html')
        
#     elif request.method == 'POST':
#         flash('Please fill out the form!')
    
#     return render_template('register.html')

# @app.route('/logout')
# def logout():
   
#    session.pop('loggedin', None)
#    session.pop('id', None)
#    session.pop('username', None)
  
#    return redirect(url_for('login'))

# @app.route('/weather_dashboard', methods=['GET', 'POST'])
# def dashboard():
#     data = None
#     if request.method == 'POST':
#         city = request.form['CityName']
#         data = get_weather(city)
#     return render_template('index.html', data=data)


# if __name__ == '__main__':
#     socketio.run(app, debug=True)


from flask import Flask, flash, render_template, request, session, redirect, url_for
from threading import Thread
import psycopg2
import psycopg2.extras
import os
import re

from backend.websocket import socketio
from backend.weather_api import main as get_weather

# Load DATABASE_URL from environment
DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    raise Exception("DATABASE_URL environment variable not set!")

# Initialize Flask app
app = Flask(__name__, template_folder='static')
app.secret_key = 'hello'

# PostgreSQL connection
conn = psycopg2.connect(DATABASE_URL)

# SocketIO setup
socketio.init_app(app)

# Routes
@app.route('/')
def home():
    if 'loggedin' in session:
        return render_template('index.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']

        cursor.execute('SELECT * FROM user_details WHERE username = %s', (username,))
        account = cursor.fetchone()

        if account and account['password'] == password:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            return redirect(url_for('dashboard'))
        else:
            flash('Incorrect username/password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        fullname = request.form.get('fullname')
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')

        cursor.execute('SELECT * FROM user_details WHERE username = %s', (username,))
        account = cursor.fetchone()

        if account:
            flash('Account already exists!')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Invalid email address!')
        elif not re.match(r'[A-Za-z0-9]+', username):
            flash('Username must contain only characters and numbers!')
        elif not username or not password or not email:
            flash('Please fill out the form!')
        else:
            cursor.execute("INSERT INTO user_details (username, password, fullname, email) VALUES (%s,%s,%s,%s)", 
                           (username, password, fullname, email))
            conn.commit()
            flash('You have successfully registered!')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/weather_dashboard', methods=['GET', 'POST'])
def dashboard():
    data = None
    if request.method == 'POST':
        city = request.form['CityName']
        data = get_weather(city)
    return render_template('index.html', data=data)

# Keep-alive logic for 24/7 running
def run_web():
    socketio.run(app, host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run_web)
    t.start()

# Only call this if running directly
if __name__ == "__main__":
    keep_alive()
