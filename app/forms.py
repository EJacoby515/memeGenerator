from flask import Blueprint, request, jsonify, render_template, flash
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Email



class UserLoginForm(FlaskForm):
    # email, password, submit
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    first_name = StringField('First Name')
    last_name =  StringField('Last Name')

    submit_button = SubmitField()

class SignUpForm(UserLoginForm):

    submit_button = SubmitField('Create Account')

class SignInForm(UserLoginForm):

    submit_button = SubmitField('Sign In')