from main import app
from flask import render_template


@app.route("/")
def hello():
    return render_template('hello.html')


@app.route("/<name>/")
def hello2(name):
    return render_template('hello.html', name=name)
