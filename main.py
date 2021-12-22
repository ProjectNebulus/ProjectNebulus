#Imports
from flask import Flask, render_template, session, flash, request, redirect
from werkzeug.utils import secure_filename
from static.python.image_to_music import *
from static.python.mongodb import *
from static.python.security import *
import os

#Variables
app = Flask('app')
app.secret_key = '12345678987654321'
@app.errorhandler(404)
def not_found(e):
  return render_template("404.html")

@app.route('/')
def index():
  return render_template("index.html")


@app.route('/dashboard')
def dashboard():

  if not session.get('username'):
    return redirect('/signin')
  else:
    new_user = request.args.get('new_user', default='false', type=str)
    if new_user == 'true':
      return render_template("dashboard.html", user = session["username"], new_account = True)
    else:
      return render_template("dashboard.html", user = session["username"])
    

@app.route("/signup")
def signup():
  return render_template("signup.html")

@app.route("/signup", methods=["POST"])
def signup_post():
  session["username"] = request.form.get("username")
  session["email"] = request.form.get("email")
  session["password"] = request.form.get("password")
  create_user(session["username"],session["email"],session["password"])
  return redirect('/dashboard?new_user=true')

@app.route("/signin")
def signin():
  return render_template("signin.html")

@app.route("/signin", methods=['POST'])
def signin_post():
  data = request.get_json()
  print(data)

  username = data['username']
  password = data['password']

  validation = check_login(username, password) #hi neel
  #cuz first we need to get it work ng, then we can make it look nice 

  if validation != "True":
    return "False"
  else:
    session['username'] = username
    session['password'] = password
    return "True"
  
  
  
  
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
