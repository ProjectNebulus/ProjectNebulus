#Imports
from flask import Flask, render_template

#Variables
app = Flask('app')

#Routing
@app.route('/')
def index():
  return render_template("index.html")

@app.route("/signup")
def signup():
  return render_template("signup.html")

@app.route("/login")
def signin():
  return render_template("login.html")
@app.route("/musiqueworld")
def musiqueworld():
  return render_template("musiqueworld.html")
#Running
app.run(host='0.0.0.0', port=8080)
