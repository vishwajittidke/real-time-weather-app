from flask import Flask
from flask_sqlalchemy import SQLAlchemy
 

app = Flask(__name__)

# POSTGRES_URL= '127.0.0.1:5000'
# POSTGRES_USER= 'postgres'
# POSTGRES_PW = 'postgres'
# POSTGRES_DB = 'weather_dashboard'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,db=POSTGRES_DB)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sample.db'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username
