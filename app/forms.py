from flask_wtf import FlaskForm
from wtforms import Stringfield, PasswordField, Submitfield, Emailfield
from wtforms.validators import InputRequired, EqualTo

class SignUpForm(FlaskForm):
    first_name = Stringfield('First Name', validators=[InputRequired()])
    last_name = Stringfield('Last Name', validators=[InputRequired()])
    username = Stringfield('Username', validators=[InputRequired()])
    email = Emailfield('Email', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    confirm_pass = PasswordField('Password', validators=[InputRequired(), EqualTo('password')])
    submit = Submitfield('Sign Up')
