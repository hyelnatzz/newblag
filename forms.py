from flask_wtf import  FlaskForm
from wtforms import StringField, PasswordField, BooleanField, HiddenField, TextAreaField, SubmitField, SelectField
from wtforms.validators import InputRequired, EqualTo, Length
from models import Category


class loginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired('email required')])
    password = PasswordField('Password', validators=[InputRequired('password field cannot be empty'), 
                                                    Length(min=8, message='password must be atleast 8 characters long')])
    remember = BooleanField('remember me?')
    next = HiddenField('')
    login = SubmitField('Login')


categories_ = [c.name for c in Category.query.all()]


class postForm(FlaskForm):
    title = StringField('Post Title', validators=[
                        InputRequired('post title required')])
    subtitle = StringField('Post Subtitle')
    category = SelectField('Select Category', choices=[
                           (name, name) for name in categories_])
    body = TextAreaField('Post Body', validators=[
                         InputRequired('password field cannot be empty')])
    tags = StringField('Post Tags')
    submit = SubmitField('Submit')

class signupForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(message='required field')] )
    email = StringField('Email', validators=[
                           InputRequired(message='required field')])
    full_name = StringField('Full Name', validators=[
                           InputRequired(message='required field')])
    dob = StringField('Date of birth', validators=[
                           InputRequired(message='required field')])
    bio = TextAreaField('Brief personal note')
    password = PasswordField('Password', validators=[InputRequired('required field'),  Length(min=8, message='password must be atleast 8 characters long')])
    confirm_password = PasswordField('Confirm password', validators=[EqualTo('password', message='password must match')])
    signup = SubmitField('Sign Up')


class categoryForm(FlaskForm):
    name = StringField('Category Name', validators=[InputRequired('post title required')])
    description = StringField('Category Description',  validators=[InputRequired('post title required')])
    create = SubmitField('Create')

class contactForm(FlaskForm):
    name = StringField('Your name', validators=[InputRequired('name required')])
    email = StringField('Email Address', validators=[InputRequired('email is required')])
    phone = StringField('Phone Number')
    message = TextAreaField('Message', validators=[InputRequired('password field cannot be empty')])
    send = SubmitField('Send')


class searchForm(FlaskForm):
    field = StringField()
    go = SubmitField('Go!')
                    
