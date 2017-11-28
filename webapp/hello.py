from flask import Flask
app = Flask(__name__)
from flask import render_template

@app.route('/')
def hello():
    return render_template('hello.html', lat=-25.363, lng=131.044)
