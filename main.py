#Imports
from flask import Flask, render_template, session, flash, request
from werkzeug.utils import secure_filename
from static.python.image_to_music import *
from static.python.mongodb import *
from static.python.security import *
import os

#Variables
app = Flask('app')
app.secret_key = '12345678987654321'
#Routing
@app.route('/')
def index():
  return render_template("index.html")

@app.route("/signup")
def signup():
  return render_template("signup.html")

@app.route("/signup", methods=["POST"])
def signup_post():
  session["username"] = request.form.get("username")
  session["email"] = request.form.get("email")
  session["password"] = request.form.get("password")
  return render_template("dashboard.html", new_account = True)

@app.route("/signin")
def signin():
  return render_template("signin.html")
  
@app.route("/musiqueworld")
def musiqueworld():
  return render_template("musiqueworld.html")

@app.route("/musiqueworld", methods=["POST"])
def musiqueworld_post():
  if 'file1' not in request.files:
      print("1")
      flash('No file part')
      return redirect(request.url)
  file = request.files['file1']
  if file.filename == '':
      print("2")
      flash('No selected file')
      return redirect(request.url)
  if file and allowed_file(file.filename):
      print("3")
      filename = secure_filename(file.filename)
      file.save(os.path.join("static/userbase/images", filename))
      resp = convert((os.path.join(UPLOAD_FOLDER, filename)))
      youtube = search_yt(songs[0]["track_name"]+" by "+songs[0]["artist_name"])
      return render_template(returned = True, youtube = youtube, resp = resp)
 
#Running
app.run(host='0.0.0.0', port=8080)
