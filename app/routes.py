from app import app
from flask import render_template
from app.forms import SignUpForm

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/add-phone")
def add_phone():
    return render_template('add_phone.html')

@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignUpForm()
    return render_template('signup.html', form=form)

@app.route("/login")
def login():
    return render_template('login.html')

@app.route('/home')
def home():
    return render_template('home.html')
