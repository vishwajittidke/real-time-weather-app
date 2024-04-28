from flask import Flask, flash, render_template, request, session, redirect, url_for
import psycopg2
import psycopg2.extras
import re 
import app


from backend.websocket import socketio
from backend.weather_api import main as get_weather



app = Flask(__name__, template_folder='static')
app.secret_key = 'hello'


DB_HOST = "localhost"
DB_NAME = "weather_db"
DB_USER = "postgres"
DB_PASS = "postgres"
 
conn = psycopg2.connect(dbname="weather_db", user="postgres", password="postgres", host="localhost")


app.config['SQLALCHEMY_DATABASE_URI'] = conn
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 



socketio.init_app(app)


@app.route('/')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        
        # User is loggedin show them the home page
        return render_template('index.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))  


@app.route('/login', methods=['GET', 'POST'])
def login():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        print(password)
 
        # Check if account exists using MySQL
        cursor.execute('SELECT * FROM user_details WHERE username = %s', (username,))
        # Fetch one record and return result
        account = cursor.fetchone()
 
        if account:
            password_rs = account['password']
            print(password_rs)
            # If account exists in user_setails table in out database
            if request.method == "POST":
                # Create session data, we can access this data in other routes
                session['loggedin'] = True
                session['id'] = account['id']
                session['username'] = account['username']
                # Redirect to home page
                return redirect(url_for('dashboard'))
            else:
                # Account doesnt exist or username/password incorrect
                flash('Incorrect username/password')
        else:
            # Account doesnt exist or username/password incorrect
            flash('Incorrect username/password')
 
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
 
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        fullname = request.form['fullname']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
    
        cursor.execute('SELECT * FROM user_details WHERE username = %s', (username,))
        account = cursor.fetchone()
        print(account)

        if account:
            flash('Account already exists!')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Invalid email address!')
        elif not re.match(r'[A-Za-z0-9]+', username):
            flash('Username must contain only characters and numbers!')
        elif not username or not password or not email:
            flash('Please fill out the form!')
        else:
            cursor.execute("INSERT INTO user_details (username, password, fullname, email) VALUES (%s,%s,%s,%s)", (username, password, fullname, email))
            conn.commit()
            flash('You have successfully registered!')
            return render_template('login.html')
        
    elif request.method == 'POST':
        flash('Please fill out the form!')
    
    return render_template('register.html')

@app.route('/logout')
def logout():
   
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
  
   return redirect(url_for('login'))

@app.route('/weather_dashboard', methods=['GET', 'POST'])
def dashboard():
    data = None
    if request.method == 'POST':
        city = request.form['CityName']
        data = get_weather(city)
    return render_template('index.html', data=data)


if __name__ == '__main__':
    socketio.run(app, debug=True)
