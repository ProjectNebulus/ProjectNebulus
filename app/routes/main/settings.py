from datetime import datetime

import flask
import google.oauth2.credentials
from googleapiclient.discovery import build

from app.static.python.mongodb import read
from app.static.python.mongodb.read import getText
from . import main_blueprint
from .spotify import (
    SPOTIPY_CLIENT_ID,
    SPOTIPY_CLIENT_SECRET,
    CacheHandler,
    FlaskSessionCacheHandler,
    SpotifyException,
    logged_in,
    render_template,
    request,
    session,
    spotipy,
)


def generate_redirect(url):
    if "nebulus" in url:
        if "https" not in url:
            return url.replace("http", "https") + "spotify"
    return url + "spotify"


@main_blueprint.route("/settings")
@logged_in
def settings():
    the_schoology = read.getSchoology(id=session.get("id"))
    the_google_classroom = read.getClassroom(session.get("id"))
    try:
        credentials = google.oauth2.credentials.Credentials(
            **flask.session["credentials"]
        )

        service = build("people", "v1", credentials=credentials)
        profile = service.people().get("people/me", personFields="names,emailAddresses")
        print(profile)
    except:
        googleclassroom = None

    try:
        credentials = google.oauth2.credentials.Credentials(
            **flask.session["credentials"]
        )
        user_info_service = build(
            serviceName="oauth2", version="v2", credentials=credentials
        )
        user_info = user_info_service.userinfo().get().execute()
        print(user_info)
        user_info = [user_info["name"], user_info["picture"]]
        googleclassroom = user_info

    except:
        user_info = None
    try:
        canvas = list(read.getCanvas(id=session.get("id")))[0].name
    except:
        canvas = None

    try:
        canvas = list(read.getCanvas(id=session.get("id")))[0].name
    except:
        canvas = []

    cache_handler = FlaskSessionCacheHandler(CacheHandler)
    spotify_auth_manager = spotipy.oauth2.SpotifyOAuth(
        scope="user-read-currently-playing playlist-modify-private",
        cache_handler=cache_handler,
        show_dialog=True,
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=generate_redirect(request.root_url),
    )
    spotify = spotipy.Spotify(auth_manager=spotify_auth_manager)

    if not spotify_auth_manager.validate_token(cache_handler.get_cached_token()):
        spotify = None
    else:
        try:
            spotify = spotify.current_user()
        except SpotifyException:
            spotify = None

    try:
        discord = list(read.getDiscord(id=session.get("id")))[0]
        discord = [
            discord.discord_user,
            discord.discord_avatar
        ]
    except:
        discord = []

    last_access = 0
    if session.get("access"):
        print(
            "Last confirmed access (seconds):",
            datetime.now().timestamp() - float(session["access"]),
        )
        last_access = datetime.now().timestamp() - float(session["access"])
    try:
        graderoom = list(read.getGraderoom(id=session.get("id")))[0]
        graderoom = [
            graderoom.username,
            graderoom.school
        ]
    except:
        graderoom = []
    try:
        github = list(read.getGithub(id=session.get("id")))[0]
        github = [
            github.username,
            github.avatar
        ]
    except:
        github = []
    return render_template(
        "user/settings.html",
        page="Nebulus - Account Settings",
        graderoom=graderoom,
        github=github,
        session=session,
        lastAccess=last_access,
        user=session.get("username"),
        user_id=session.get("id"),
        pswHashes="*" * session.get("pswLen"),
        email=session.get("email"),
        avatar=session.get("avatar", "/static/images/nebulusCats/v3.gif"),
        schoology=the_schoology,
        classroom=the_google_classroom,
        googleclassroom=user_info,
        canvas=canvas,
        spotify=spotify,
        discord=discord,
        translate=getText,
        points=read.find_user(id=session.get("id")).points,
    )
