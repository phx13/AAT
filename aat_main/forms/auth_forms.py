from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, StringField, PasswordField


class LoginForm(FlaskForm):
    email = StringField('Email')
    password = PasswordField('Password')
    submit = SubmitField('Submit')
