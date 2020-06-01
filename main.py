from flask import Flask, render_template, session, request, flash, redirect, make_response
from flask_sqlalchemy import SQLAlchemy
from hashpassword import makePasswordHash, checkPasswordHash
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
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50))
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    height = db.Column(db.String(6))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(50))
    currentWeight = db.Column(db.Integer)
    goalWeight = db.Column(db.Integer)
    date_created = db.Column(db.DateTime, default=datetime.now)


class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    name = db.Column(db.String(50))
    serving = db.Column(db.Integer)
    calories = db.Column(db.Integer)
    macromolecules = db.Column(db.String(50))
    date_created = db.Column(db.DateTime, default=datetime.now)

class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    name = db.Column(db.String(50))
    sets = db.Column(db.Integer)
    reps = db.Column(db.Integer)
    time = db.Column(db.Integer)
    date_created = db.Column(db.DateTime, default=datetime.now)


@app.before_request
def requireLogin():
    allowed_routes = ['login', 'signup']
    if request.endpoint not in allowed_routes and 'username' not in session:
        flash('Please login or sign up to access the rest of the features!', 'error')
        return redirect('/login') 


@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = request.json
    else:
        resp = make_response(render_template('home.html'))
        resp.set_cookie('Name', str(session['lastname'] + ', ' + session['firstname']))
        return resp

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        username = data['username']
        password = data['password']
        
        user = db.session.query(User).filter(User.username==username).first()
        if user:
            if checkPasswordHash(password, user.password):
                session['username'] = username
                session['firstname'] = user.firstname
                session['lastname'] = user.lastname
                return redirect('/')
            else:
                flash('The user doesn\'t exist or the password provided was incorrect', 'error')
                return redirect('/login')   

        else:
            flash('The user doesn\'t exist or the password provided was incorrect', 'error')
            return redirect('/login')   
    else:
        return render_template('login.html')

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    if request.method == 'POST':
        data = request.form
        username = data['username']
        email = data['email']
        password = data['password']
        confirmPassword = data['confirmPassword']
        if password == confirmPassword:
            matchingUsernames = False
            #matchingUsernames = db.session.query(User).filter(User.username==username).first()
            if matchingUsernames:
                flash('Username already exists!', 'error')
                return redirect('/signup')
            else:
                matchingEmail = False
                #matchingEmail = db.session.query(User).filter(User.email==email).first()
                if matchingEmail:
                    flash('Email is already registered with another account!', 'error')
                    return redirect('/signup')
                else:
                    firstname = data['firstName']
                    lastname = data['lastName']
                    age = data['age']
                    gender = data['gender']
                    currentWeight = data['currentWeight']
                    goalWeight = data['goalWeight']
                    height = data['height']
                    user = User(username=username, email=email, firstname=firstname, lastname=lastname, 
                    password = makePasswordHash(password), height=height, age=age, gender=gender, currentWeight=currentWeight,
                    goalWeight=goalWeight)
                    #db.session.add(user)
                    #db.session.commit()

                    session['username'] = username
                    session['firstname'] = firstname
                    session['lastname'] = lastname
                    return redirect('/')

        else:
            flash('Passwords didn\'t match!', 'error')
            return redirect('/signup')

    else:
        return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('firstname', None)
    session.pop('lastname', None)
    return redirect('/login')

@app.route('/resources')
def credits():
    return render_template('resources.html')


@app.route('/exercise')
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

