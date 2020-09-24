from flask_wtf import  FlaskForm
from wtforms import StringField, PasswordField, BooleanField, DateField, TextAreaField, SubmitField
from wtforms.validators import InputRequired, EqualTo, Length


class loginForm(FlaskForm):
    email = StringField('email', validators=[InputRequired('email required')])
    password = PasswordField('password', validators=[InputRequired('password field cannot be empty'), 
                                                    Length(min=8, message='password must be atleast 8 characters long')])
    login = SubmitField('Login')


class signupForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(message='required field')] )
    email = StringField('email', validators=[
                           InputRequired(message='required field')])
    full_name = StringField('full name', validators=[
                           InputRequired(message='required field')])
    
                    
