from flask import Flask, render_template, session, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import datetime

app = Flask(__name__)

app.config['SECRET_KEY'] = 'hello'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'


db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50))
    date_created = db.Column(db.DateTime, default=datetime.now)
    height = db.Column(db.String(6), unique = False)
    currentWeight = db.Column(db.String(3), unique = False)
    goalWeight = db.Column(db.String(3), unique = False)

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/resources')
def credits():
    return render_template('credits.html')


@app.route('/exersise')
def exersise():
    return render_template('exersise.html')

@app.route('/food')
def food():
    return render_template('food.html')

@app.route('/run')
def run():
    return render_template('run.html')

@app.route('/api/exersises')
def exerises():
    with open ('data/exersises.json','r') as read_file:
        return read_file.read()

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/analytics')
def analytics():
    return render_template('analytics.html')
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

