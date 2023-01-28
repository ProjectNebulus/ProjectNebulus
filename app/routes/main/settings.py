from datetime import datetime

import flask
import google.oauth2.credentials
from googleapiclient.discovery import build

from app.static.python.mongodb import read
from app.static.python.mongodb.read import get_text
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
    schoology = read.get_schoology(id=session["id"])
    google_classroom = read.get_classroom(session["id"])
    try:
        credentials = google.oauth2.credentials.Credentials(
            **flask.session["credentials"]
        )

        service = build("people", "v1", credentials=credentials)
        profile = service.people().get("people/me", personFields="names,emailAddresses")
        print(profile)
    except:
        google_classroom = None

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
        google_classroom = user_info

    except:
        user_info = None
    try:
        canvas = list(read.get_canvas(id=session["id"]))[0].name
    except (TypeError, IndexError):
        canvas = None

    try:
        canvas = list(read.get_canvas(id=session["id"]))[0].name
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
        discord = list(read.get_discord(id=session["id"]))[0]
        discord = [discord.discord_user, discord.discord_avatar]
    except (TypeError, IndexError):
        discord = []

    last_access = 10000
    if session.get("access"):
        last_access = datetime.now().timestamp() - float(session["access"])

        if last_access > 60 * 60:
            del session["access"]

        print("Last confirmed access (seconds):", last_access)

    try:
        graderoom = list(read.get_graderoom(id=session["id"]))[0]
        graderoom = [graderoom.username, graderoom.school]
    except (TypeError, IndexError):
        graderoom = []

    try:
        github = list(read.get_github(id=session["id"]))[0]
        github = [github.username, github.avatar]
    except (TypeError, IndexError):
        github = []

    schools = []
    import json

    try:
        rawschool = list(read.get_schools(session["id"]))
        myjson = list(json.load(open("app/schools.json")))
        for school in myjson:
            if school["code"] in rawschool:
                schools.append(school)

    except (TypeError, IndexError):
        schools = []

    return render_template(
        "user/settings.html",
        page="Nebulus - Account Settings",
        graderoom=graderoom,
        github=github,
        session=session,
        lastAccess=last_access,
        user=session.get("username"),
        user_id=session["id"],
        pswHashes="*" * session.get("pswLen"),
        email=session.get("email"),
        avatar=session.get("avatar", "/static/images/nebulusCats/v3.gif"),
        schoology=schoology,
        classroom=google_classroom,
        googleclassroom=user_info,
        schools=schools,
        canvas=canvas,
        spotify=spotify,
        discord=discord,
        translate=get_text,
        points=read.find_user(id=session["id"]).points,
    )
