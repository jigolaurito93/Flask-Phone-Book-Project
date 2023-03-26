from app import app
from flask import render_template, redirect, url_for, flash
from app.forms import SignUpForm, LoginForm

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/add-phone")
def add_phone():
    return render_template('add_phone.html')

@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        print('Successfully Signed Up..')
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        username = form.username.data
        password = form.password.data
        print(first_name, last_name, email, username, password)
        flash(f"Thank you {first_name} for signing up!", "success")
        return redirect(url_for('index'))
    return render_template('signup.html', form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print('Successfull Logged In..')
        username = form.username.data
        password = form.password.data
        print(username, password)
        # TODO: Check if there is a user with username and that password
        #Fake an invalid log in
        if password == 'abc':
            flash('Invalid username and/or password. Please try again', 'danger')
            return redirect(url_for('login'))

        flash(f'You have succesfully logged in as {username}!', 'success')
        return redirect(url_for('index'))
    return render_template('login.html', form=form)

@app.route('/home')
def home():
   
    return render_template('home.html')
