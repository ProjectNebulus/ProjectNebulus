#Imports
from flask import Flask, render_template

#Variables
app = Flask('app')

#Routing
@app.route('/')
def index():
  return render_template("index.html")

#Running
app.run(host='0.0.0.0', port=8080)
