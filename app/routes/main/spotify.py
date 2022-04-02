from flask import render_template, redirect, session
from . import main_blueprint
import os
from flask import Flask, session, request, redirect
from flask_session import Session
import spotipy
from .utils import logged_in
import uuid
from app.static.python.mongodb import read, update

# In order to get Spotipy to work, you must install the latest version with cloning the repo with the following command:
# pip3 install git+https://github.com/plamere/spotipy
SPOTIPY_CLIENT_ID = "846095b9ce934b0da3e0aaf3adbf600c"
SPOTIPY_CLIENT_SECRET = "1d79c77cee124d8f8e20b16f720d65e8"
SPOTIPY_REDIRECT_URI = "http://localhost:8080/spotify"

caches_folder = "./.spotify_caches/"
if not os.path.exists(caches_folder):
    os.makedirs(caches_folder)


def fetch_cache():
    cache = read.getSpotifyCache(username=session["username"])
    if cache is None:
        return {}
    return cache


def update_cache():
    return


def get_path():
    cache = fetch_cache()
    folder = caches_folder + session.get("uuid")
    with open(folder, "w") as thefolder:
        print(cache, file=thefolder)
    return folder


@main_blueprint.route("/spotify")
@logged_in
def spotify():
    if not session.get("uuid"):
        # Step 1. Visitor is unknown, give random ID
        import uuid

        session["uuid"] = str(uuid.uuid4())

    cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=get_path())
    auth_manager = spotipy.oauth2.SpotifyOAuth(
        scope="user-read-currently-playing playlist-modify-private",
        cache_handler=cache_handler,
        show_dialog=True,
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
    )

    if request.args.get("code"):
        # Step 3. Being redirected from Spotify auth page
        auth_manager.get_access_token(request.args.get("code"))
        print(auth_manager)
        print(cache_handler)
        return redirect("/spotify")

    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        # Step 2. Display sign in link when no token
        auth_url = auth_manager.get_authorize_url()
        return render_template("connectSpotify.html", auth=True, auth_url=auth_url)

    # Step 4. Signed in, display data
    uuid = session["uuid"]
    cache = fetch_cache()
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    return render_template("connectSpotify.html", spotify=spotify, auth=False)


@main_blueprint.route("/spotify/sign_out")
def spotify_sign_out():
    try:
        # Remove the CACHE file (.cache-test) so that a new user can authorize.
        os.remove(get_path())
        session.pop("uuid")
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))
    return redirect("/spotify")


@main_blueprint.route("/spotify/playlists")
def spotify_playlists():
    cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=get_path())
    auth_manager = spotipy.oauth2.SpotifyOAuth(
        scope="user-read-currently-playing playlist-modify-private",
        cache_handler=cache_handler,
        show_dialog=True,
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
    )

    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect("/spotify")

    spotify = spotipy.Spotify(auth_manager=auth_manager)
    return spotify.current_user_playlists()


@main_blueprint.route("/spotify/currently_playing")
def currently_playing():
    cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=get_path())
    auth_manager = spotipy.oauth2.SpotifyOAuth(
        scope="user-read-currently-playing playlist-modify-private",
        cache_handler=cache_handler,
        show_dialog=True,
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
    )

    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect("/spotify")
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    track = spotify.current_user_playing_track()
    if not track is None:
        return track
    return "No track currently playing."


@main_blueprint.route("/spotify/current_user")
def spotify_current_user():
    cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=get_path())
    auth_manager = spotipy.oauth2.SpotifyOAuth(
        scope="user-read-currently-playing playlist-modify-private",
        cache_handler=cache_handler,
        show_dialog=True,
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
    )

    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect("/spotify")
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    return spotify.current_user()


"""
Following lines allow main_blueprintlication to be run more conveniently with
`python main_blueprint.py` (Make sure you're using python3)
(Also includes directive to leverage pythons threading capacity.)
"""
if __name__ == "__main__":
    main_blueprint.run(threaded=True, port=int(os.environ.get("PORT", 9080)))
