
#Imports
from flask import Flask, render_template, session, flash, request, redirect
from werkzeug.utils import secure_filename
from static.python.image_to_music import *
from static.python import mongodb as db
from static.python import security
import os
import re


regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
#Variables
app = Flask('app')
app.secret_key = '12345678987654321'

#app routes
@app.errorhandler(404)
def not_found(e):
  return render_template("404.html", page='404 Not Found')

@app.errorhandler(500)
def server_error(e):
  return render_template("500.html", page="500 Internal Server Error")

@app.route('/new')
def new():
   return render_template("new_course.html", page='Nebulus - New Course')

@app.route('/new', methods=['POST'])
def new_post():
  data = request.get_json()
  db.create_course(data['name'], data['teacher'], session['username'])
  return 'success'

@app.route('/')
def index():
  if session.get("username"):
    return redirect('/dashboard')
  else:
    return render_template("index.html", page='Nebulus')

@app.route("/chat")
def chat():
  return render_template("chat.html", page='Nebulus - Chat') 

@app.route('/logout')
def logout():
  session['username'] = None
  session['email'] = None
  session['password'] = None
  return redirect('/')

@app.route("/profile")
def profile():
  if session.get("username"):
    return render_template("profile.html", page="Nebulus - Profile", user=session["username"])
  else:
    return redirect("/signin")

@app.route('/settings')
def settings():
  return render_template("settings.html", page='Nebulus - Account Settings')
  
@app.route('/dashboard')
def dashboard():
  if not session.get('username') and not session.get('email'):
    return redirect('/signin')
  else:
    new_user = request.args.get('new_user', default='false', type=str)
    return render_template("dashboard.html", user = session["username"], db=db, page='Nebulus - Dashboard', new_account = new_user == 'true')

@app.route("/developers")
def developers():
  return render_template("developers.html", page='Nebulus - Developers') 

@app.route("/signup")
def signup():
  if session.get("username"):
    return redirect('/dashboard')
  return render_template("signup.html", page = 'Nebulus - Sign Up')

@app.route("/signup", methods=["POST"])
def signup_post():
  session["username"] = request.form.get("username")
  session["email"] = request.form.get("email")
  session["password"] = request.form.get("password") 
  if ( not db.create_user(session['username'], session['email'], session['password'])):
    pass
  else:
    return redirect('/dashboard?new_user=true')

@app.route("/signin")
def signin():
  if not session.get('username'):
    return render_template("signin.html", page='Nebulus - Log In')
  return redirect('/dashboard')

@app.route("/signin", methods=['POST'])
def signin_post():
  json = request.get_json()
  validation = db.check_login(json.get('username'), json.get('password'))
  
  """
  Status codes:
  0 - Login Successful
  1 - Invalid Password
  2 - Username does not exist
  """
  if validation == "0":
    session['username'] = json.get('username')
    session['password'] = json.get('password')
    
    if re.fullmatch(regex, session['username']):
      session['email'] = session['username']
      session['username'] = db.Accounts.find_one({'email': session['email']})['username']
    else:
      session['email'] = db.Accounts.find_one({'username': session['username']})['email']
    
      
  
  return validation
    
@app.route("/musiqueworld")
def musiqueworld():
  return render_template("musiqueworld.html", page = "Nebulus - Musiqueworld")

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
