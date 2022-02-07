# Imports
from dotenv import load_dotenv #Exportng Environment Variables in the .env file
load_dotenv()
from flask import Flask, render_template, session, flash, request, redirect
from werkzeug.utils import secure_filename
from static.python.image_to_music import *
from static.python import mongodb as db
from static.python.spotify import status as spotifystatus
from static.python.youtube import search_yt
import os
import re

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
# Variables
app = Flask('app')
app.secret_key = '12345678987654321'

check_user_params = True

# app routes
@app.route("/developers")
def developers():
  return render_template("developerportal.html", user=session.get("username"), db=db, page = "Nebulus - Developer Portal", developer=True)

@app.route("/developers/api")
def api_docs():
  return " "

@app.route("/spoistatus", methods=["POST"])
def spotify_status():
    a = spotifystatus()
    string = ""
    if len(string) >= 1:
      string = a[0] + " - " + a[1]
    else:
      string = "You aren't listening to anything!"
    return string

@app.route("/profile")
def profile():
    return render_template("user/profile.html", page="Nebulus - Profile", user=session.get("username"))


@app.errorhandler(404)
def not_found(e):
    return render_template("errors/404.html", page='404 Not Found')


@app.errorhandler(500)
def server_error(e):
    return render_template("errors/500.html", page="500 Internal Server Error", e=e)


@app.route('/courses/<id>')
def courses(id):
    if session.get("username") and session.get('password'):
        courses = db.Accounts.find_one({'username': session.get("username")})["courses"]

        for course in courses:
            if course.get('_id') == id:
                break

        return render_template("courses/course.html", page="Nebulus - " + course.get("name", "Courses"), db=db, course=course,
                               user=session.get("username"))

    else:
        return redirect('/signin')


@app.route('/new')
def new():
    return render_template("courses/new.html", page='Nebulus - New Course')


@app.route('/new', methods=['POST'])
def new_post():
    data = request.get_json()
    db.create_course(data['name'], data['teacher'], session.get("username"))
    return 'success'


@app.route('/')
def index():
    if session.get("username"):
        return redirect('/dashboard')
    else:
        return render_template("main/index.html", page='Nebulus | Learning, All in One.', user=session.get("username"))


@app.route("/chat")
def chat():
    return render_template("chat.html", page='Nebulus - Chat', session=session)


@app.route('/logout')
def logout():
    session['username'] = None
    session['email'] = None
    session['password'] = None
    return redirect('/')


@app.route('/settings')
def settings():
    return render_template("user/settings.html", page='Nebulus - Account Settings', session=session, user=session.get("username"))


@app.route('/dashboard')
def dashboard():
    # if the user is not logged in, redirect to the login page
    if not (session.get('username') and session.get('password')):
        return redirect('/signin')
    else:
        new_user = request.args.get('new_user', default='false', type=str)
        return render_template("dashboard.html", user=session["username"], email=session["email"], db=db, page='Nebulus - Dashboard', new_account=new_user == 'true')


@app.route("/about")
def about():
    return render_template("about.html", page='Nebulus - About Us', user=session.get("username"))


@app.route("/lms")
def lms():
    if not (session.get('username') and session.get('password')):
        return redirect('/signin')
    else:
        new_user = request.args.get('new_user', default='false', type=str)
        return render_template("lms.html", user=session["username"], db=db, page='Nebulus - Dashboard', new_account=new_user == 'true')


@app.route("/music")
def music():
    return render_template("music.html", page='Nebulus - Music', user=session.get("username"))

@app.route("/holidays")
def vh():
    return render_template("holidays.html", page='Nebulus - Virtual Holidays', user=session.get("username"))


@app.route("/signup")
def signup():
    # If the user is already logged in, redirect to the dashboard
    if session.get("username") and session.get('password'):
        return redirect('/dashboard')
    return render_template("main/signup.html", page='Nebulus - Sign Up', disablebar=True)


@app.route("/signup", methods=["POST"])
def signup_post():
    data = request.get_json()
    validation = db.create_user(data['username'], data['email'], data['password'])
    if validation == '0':
        session["username"] = data.get("username")
        session["email"] = data.get("email")
        session["password"] = data.get("password")
    return validation



@app.route("/signin")
def signin():
    # If the user is already logged in, redirect to the dashboard
    if not session.get('username') and session.get('password'):
        if check_user_params and session.get("email"):
            db.check_user_params(session.get("email"))

        return render_template("main/signin.html", page='Nebulus - Log In', disablebar=True)

    return redirect('/dashboard')


@app.route("/signin_username", methods=['POST'])
def signin_username():
    json = request.get_json()
    validation = db.check_user(json.get('username'))
    if validation == 'true':
        session["username"] = json.get('username')
        if re.fullmatch(regex, session['username']):
            # If the username is an email, then we need to get the username from the database
            session['email'] = session['username']
            session['username'] = db.Accounts.find_one({'email': session['email']})['username']
        else:
            # If the username is not an email, then we need to get the email from the database
            session['email'] = db.Accounts.find_one({'username': session['username']})['email']
    return validation

@app.route("/signin_password", methods=['POST'])
def signin_password():
    json = request.get_json()
    validation = db.check_password(session['email'], json.get('password'))
    return validation

@app.route("/signin", methods=['POST'])
def signin_post():
    data = request.get_json()
    session["password"] = data.get("password")
    return 'success'

@app.route("/musiqueworld")
def musiqueworld():
    return render_template("musiqueworld/layout.html", page="Nebulus - Musiqueworld")


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
        youtube = search_yt(songs[0]["track_name"] + " by " + songs[0]["artist_name"])
        return render_template(returned=True, youtube=youtube, resp=resp)


# Running
app.run(host='0.0.0.0', port=8080)
