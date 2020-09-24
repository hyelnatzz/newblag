from flask import Flask,render_template,request


app=Flask(__name__)
app = Flask(__name__)
app.config.from_pyfile('config.py')



@app.route('/',methods=['GET','POST'])
def home():
    if request.method=='POST':
        return render_template('index.html')
    return render_template('index.html')

if __name__ == '__main__':
    app.run(port=5000,debug=True)
