import os
from datetime import datetime
from flask import flash, redirect,render_template,request
from flask.helpers import url_for
from flask_admin.contrib.sqla.view import ModelView
from flask_bootstrap import Bootstrap
from models import Post, Category, User
from flask_sqlalchemy import  SQLAlchemy
from forms import loginForm, signupForm, categoryForm, contactForm, searchForm, categories_,postForm
from flask_admin import Admin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from models import db, app


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

########################################################################################
def format_date(t):
    t = datetime.strptime(t[:-7], '%Y-%m-%d %H:%M:%S%f')
    f_t = datetime.strftime(t, '%B %d, %Y at %I:%M %p')
    return f_t


@app.route('/', methods=['GET','POST'])
def index():
    categories = Category.query.all()
    posts = Post.query.filter_by(published=1)
    d = {i.id:format_date(i.date_created) for i in posts}
    return render_template('index.html', current_user=current_user, categories=categories, posts=posts, times = d)

@app.route('/user/')
@login_required
def userDashboard():
    user_posts = current_user.posts 
    total_posts = len(user_posts)
    published_posts = len([i for i in user_posts if i.published == 1])
    unpublished_posts = len([i for i in user_posts if i.published == 0])
    return render_template('dashboard.html', user= current_user, posts=user_posts, total_posts=total_posts, published_posts=published_posts, unpublished_posts = unpublished_posts)

@app.route('/signup/', methods=['GET','POST'])
def signup():
    form = signupForm()
    search = searchForm()
    date = datetime.strftime(datetime.now(), '%d/%m/%Y')
    categories = Category.query.all()
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
        flash('Registration successfull, you can now login')
        return redirect(url_for('index'))
    return render_template('signup.html', form=form, search=search, date=date, categories=categories_, current_user=current_user, cat=categories)


@app.route('/login/', methods=['POST', 'GET'])
def login():
    form = loginForm()
    search = searchForm()
    categories = Category.query.all()
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
                return render_template('login.html', form=form, search=search, categories=categories, current_user=current_user)
        else: 
            flash('email not registered')
    form.next.data = request.args.get('next')
    return render_template('login.html', form=form, search=search, categories = categories, current_user=current_user)


@app.route('/logout/')
def logout():
    logout_user()
    return redirect( url_for('index') )

@app.route('/post/<int:post_id>/', methods=['GET'])
def post(post_id):
    search = searchForm()
    categories = Category.query.all()
    post = Post.query.filter_by(id=post_id).one()
    t = datetime.strptime(post.date_created[:-7], '%Y-%m-%d %H:%M:%S%f')
    f_t = datetime.strftime(t, '%B %d, %Y at %I:%M %p')
    return render_template('post.html', post=post, date_created=f_t, current_user=current_user, categories=categories)


@app.route('/post/new/', methods=['GET','POST'])
@login_required
def createPost():
    form = postForm()
    search = searchForm()
    categories = Category.query.all()
    if form.validate_on_submit():
        post = Post()
        post.title = form.title.data.strip()
        post.subtitle = form.subtitle.data.strip()
        category = db.session.query(Category).filter_by(name=form.category.data).one()
        post.category = category
        post.author = current_user
        post.body = form.body.data.strip()
        post.tags = form.tags.data.strip()
        db.session.add(post)
        db.session.commit()
        flash('Post Created Successfully')
        return redirect( url_for('post', post_id = post.id) )
    return render_template('newpost.html', form=form, search=search, categories=categories_, cat=categories)


@app.route('/post/edit/<int:post_id>/', methods=['GET', 'POST'])
@login_required
def editPost(post_id):
    form = postForm()
    search = searchForm()
    post = db.session.query(Post).filter_by(id=post_id).one()
    if form.validate_on_submit():
        post.title = form.title.data.strip()
        post.subtitle = form.subtitle.data.strip()
        category = db.session.query(Category).filter_by(
            name=form.category.data).one()
        post.category = category
        post.body = form.body.data.strip()
        post.tags = form.tags.data.strip()
        db.session.add(post)
        db.session.commit()
        flash('Post Updated Successfully')
        return redirect(url_for('post', post_id=post.id))
    print(post.body)
    return render_template('editpost.html', form=form, search=search, categories=categories_, post=post)



@app.route('/post/delete/<int:post_id>/')
@login_required
def deletePost(post_id):
   return 'delete post page'


@app.route('/category/<int:category_id>/')
def category(category_id):
    cat = Category.query.filter_by(id=category_id).one()
    members= list(filter(lambda x: x.published, cat.members))
    return render_template('category.html', category=cat, posts=members)


@app.route('/search/')
def search():
   return 'search results page'

@app.route('/categories/')
def categories():
    search = searchForm()
    categories = Category.query.all()
    lengths = {i.name:len(list(filter(lambda x: x.published, i.members))) for i in categories}
    return render_template('categories.html', categories=categories, lengths=lengths, search=search)








if __name__ == '__main__':
    app.run()
