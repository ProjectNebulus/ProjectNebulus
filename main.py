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

@app.route("/signin")
def signin():
  return render_template("signin.html")
#Running
app.run(host='0.0.0.0', port=8080)
