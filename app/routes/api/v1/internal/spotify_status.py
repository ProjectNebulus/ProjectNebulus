from . import internal
from ....main.utils import private_endpoint
from .....static.python.spotify import get_song


@internal.route("/spotify-status", methods=["POST"])
def spotify_status():
    song = get_song()
    if len(song) == 4:
        the_song = song[0]
        artist = song[1]
        art = song[2]
        art2 = song[3]
        string = the_song + " • " + artist + " • " + art + " • " + art2
    else:
        string = "You aren't listening to anything!"
    return string
