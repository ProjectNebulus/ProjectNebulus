import datetime

from flask import render_template, redirect, session
from spotipy import CacheHandler

from . import main_blueprint
import os
from flask import Flask, session, request, redirect
from flask_session import Session
import spotipy
from .utils import logged_in
import uuid

# In order to get Spotipy to work, you must install the latest version with cloning the repo with the following command:
# pip3 install git+https://github.com/plamere/spotipy
SPOTIPY_CLIENT_ID = "846095b9ce934b0da3e0aaf3adbf600c"
SPOTIPY_CLIENT_SECRET = "1d79c77cee124d8f8e20b16f720d65e8"
# SPOTIPY_REDIRECT_URI = "http://localhost:8080/spotify"

caches_folder = "./.spotify_caches/"
if not os.path.exists(caches_folder):
    os.makedirs(caches_folder)


def generate_redirect(url):
    if "nebulus" in url:
        if "https" not in url:
            return url.replace("http", "https") + "spotify"
    return url + "spotify"


class FlaskSessionCacheHandler(CacheHandler):
    """
    A cache handler that stores the token info in the session framework
    provided by Django.
    Read more at https://docs.djangoproject.com/en/3.2/topics/http/sessions/
    """

    def __init__(self, request):
        """
        Parameters:
            * request: HttpRequest object provided by Django for every
            incoming request
        """
        self.request = request

    def get_cached_token(self):
        token_info = None
        try:
            token_info = session["token_info"]
        except KeyError:
            print("Token not found in the session")

        return token_info

    def save_token_to_cache(self, token_info):
        try:
            session["token_info"] = token_info
        except Exception as e:
            print("Error saving token to cache: " + str(e))


@main_blueprint.route("/spotify")
@logged_in
def spotify():
    if not session.get("uuid"):
        # Step 1. Visitor is unknown, give random ID
        session["uuid"] = str(uuid.uuid4())

    cache_handler = FlaskSessionCacheHandler(CacheHandler())
    SPOTIPY_REDIRECT_URI = generate_redirect(request.root_url)
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
        return redirect("/spotify")

    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        # Step 2. Display sign in link when no token
        auth_url = auth_manager.get_authorize_url()
        return redirect(auth_url)

    # Step 4. Signed in, display data
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    return render_template("connectSpotify.html", spotify=spotify, auth=False)


@main_blueprint.route("/spotify/sign_out")
def spotify_sign_out():
    try:
        # Remove the CACHE file (.cache-test) so that a new user can authorize.
        session.pop("token_info")
        session.pop("uuid")
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))
    return redirect("/spotify")


@main_blueprint.route("/spotify/playlists")
def spotify_playlists():
    cache_handler = FlaskSessionCacheHandler(CacheHandler())
    SPOTIPY_REDIRECT_URI = generate_redirect(request.root_url)
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
    cache_handler = FlaskSessionCacheHandler(CacheHandler)
    SPOTIPY_REDIRECT_URI = generate_redirect(request.root_url)
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
        import time
        timestamp =  int(time.time()) - int(track["timestamp"]//1000)
        print(timestamp)
        name = track["item"]["name"]
        artists = []
        explicit = track["item"]["explicit"]
        for i in track["item"]["artists"]:
            artists.append(i["name"])
        image = track["item"]["album"]["images"][0]["url"]
        album = track["item"]["album"]["name"]

        playing = track["is_playing"]
        return f"""
        {name} by {artists} on {album}
        Explicit: {explicit}<br>
        <img src="{image}" style="height:100px;border-radius:10%;"><br>
        
        Track is playing? {playing}
        {timestamp/10} seconds remaining!
        """

    return "No track currently playing."


@main_blueprint.route("/spotify/current_user")
def spotify_current_user():
    cache_handler = FlaskSessionCacheHandler(CacheHandler)
    SPOTIPY_REDIRECT_URI = generate_redirect(request.root_url)
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
