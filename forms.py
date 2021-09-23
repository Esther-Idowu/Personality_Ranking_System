# Pylance: reportMissingImports=false
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.fields.core import SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import Recruiter, Applicants


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=  2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    #user_type = SelectField()
    user_type = SelectField(label='user_type', choices=[("Applicants"), ("Recruiter")])
    submit = SubmitField('Sign Up')
    #userr = user_type.data
    

    def validate_username(self, username):
        print(self)
        print(self.user_type.data, "usertyprrr")
        user1= self.user_type.data
        var = {"Applicants" : Applicants, "Recruiter" : Recruiter }
        user = var[user1].query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        var = {"Applicants" : Applicants, "Recruiter" : Recruiter }
        user1= self.user_type.data
        user = var[user1].query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')



class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    user_type = SelectField(label='user_type', choices=[("Applicants"), ("Recruiter")])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')