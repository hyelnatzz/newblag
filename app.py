from re import search
from flask import Flask,render_template,request



app = Flask(__name__)
app.config.from_pyfile('config.py')



@app.route('/', methods=['GET','POST'])
def index():
    return render_template('index.html')

@app.route('/user/')
def userDashboard():
   return 'user dashboard'

@app.route('/signup/')
def signup():
   return 'signup page'

@app.route('/login/')
def login():
   return 'login page'


@app.route('/post/<int:post_id>/')
def post(post_id):
   return 'view post page'

@app.route('/post/new/')
def createPost():
   return 'create post page'


@app.route('/post/edit/<int:post_id>/')
def editPost(post_id):
   return 'edit post page'


@app.route('/post/delete/<int:post_id>/')
def deletePost(post_id):
   return 'delete post page'


@app.route('/category/<int:category_id>/')
def category(category_id):
   return 'category page'


@app.route('/search/<str:search_term>/')
def search():
   return 'search results page'

@app.route('/categories/')
def categories():
   return 'categories page'








if __name__ == '__main__':
    app.run()
