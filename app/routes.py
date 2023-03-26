from app import app
from flask import render_template

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/add-phone")
def add_phone():
    return render_template('add_phone.html')

@app.route("/signup")
def signup():
    return render_template('signup.html')

@app.route("/login")
def login():
    return render_template('login.html')

@app.route('/home')
def home():
    return render_template('home.html')
