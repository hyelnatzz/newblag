import os
from datetime import datetime
from flask import Flask, flash, redirect,render_template,request
from flask.helpers import url_for
from flask_admin.contrib.sqla.view import ModelView
from flask_bootstrap import Bootstrap
from models import Post, Category, User
from flask_sqlalchemy import  SQLAlchemy
from forms import loginForm, signupForm, categoryForm, contactForm, searchForm
from flask_admin import Admin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_required, login_user, logout_user, current_user


app = Flask(__name__)
app.config.from_pyfile('config.py')
app.config['SECRET_KEY'] = os.urandom(8).hex()
db = SQLAlchemy(app)
Bootstrap(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

admin = Admin(app)
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Category, db.session))
admin.add_view(ModelView(Post, db.session))


@login_manager.user_loader
def load(user_id):
    return User.query.get(int(user_id))


###########################################################################################
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField,SubmitField
from wtforms.validators import InputRequired
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
########################################################################################


@app.route('/', methods=['GET','POST'])
def index():
    return render_template('index.html')

@app.route('/user/')
@login_required
def userDashboard():
   return render_template('dashboard.html', user= current_user)

@app.route('/signup/', methods=['GET','POST'])
def signup():
    form = signupForm()
    search = searchForm()
    date = datetime.strftime(datetime.now(), '%d/%m/%Y')
    if form.validate_on_submit():
        user = User()
        user.username = form.username.data.strip()
        if db.session.query(User).filter_by(username=user.username).first():
            flash(f'"{user.username}" username already taken.')
            return redirect( url_for('signup'))
        user.full_name = form.full_name.data.strip()
        user.email = form.email.data.strip()
        if db.session.query(User).filter_by(email=user.email).first():
            flash(f'"{user.email}" email already taken.')
            return redirect(url_for('signup'))
        user.bio = form.bio.data.strip()
        user.dob = form.dob.data.strip()
        user.password = generate_password_hash(form.password.data.strip(), method='sha256')
        db.session.add(user)
        db.session.commit()
        return f'{user.username} Success'
    return render_template('signup.html', form=form, search=search, date=date, categories=categories_)
next_ = True

@app.route('/login/', methods=['POST', 'GET'])
def login():
    form = loginForm()
    search = searchForm()
    if form.validate_on_submit():
        email = form.email.data.strip()
        password = form.password.data.strip()
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=form.remember)
                print(form.next.data)
                return redirect(form.next.data or url_for('index') )
            else:
                flash('Invalid password')
                return render_template('login.html', form=form, search=search, categories=categories_)
        else: 
            flash('email not registered')
    form.next.data = request.args.get('next')
    return render_template('login.html', form=form, search=search, categories = categories_)


@app.route('/logout/')
def logout():
    logout_user()
    return redirect( url_for('index') )

@app.route('/post/<int:post_id>/', methods=['GET'])
def post(post_id):
    search = searchForm()
    return render_template('post.html')


@app.route('/post/new/', methods=['GET','POST'])
@login_required
def createPost():
    form = postForm()
    search = searchForm()
    if form.validate_on_submit():
        post = Post()
        post.title = form.title.data.strip()
        post.subtitle = form.subtitle.data.strip()
        category = db.session.query(Category).filter_by(name=form.category.data).one()
        author = db.session.query(User).filter_by(id=current_user.id).one()
        post.category = category
        post.author = author
        post.body = form.body.data.strip()
        post.tags = form.tags.data.strip()
        db.session.add(post)
        db.session.commit()
        flash('Post Created Successfully')
        return redirect( url_for('createPost') )
    return render_template('newpost.html', form=form, search=search, categories=categories_)


@app.route('/post/edit/<int:post_id>/')
def editPost(post_id):
   return 'edit post page'


@app.route('/post/delete/<int:post_id>/')
def deletePost(post_id):
   return 'delete post page'


@app.route('/category/<int:category_id>/')
def category(category_id):
    cat = Category.query.filter_by(id=category_id).one()
    return render_template('category.html', category=cat)


@app.route('/search/')
def search():
   return 'search results page'

@app.route('/categories/')
def categories():
   return 'categories page'








if __name__ == '__main__':
    app.run()
