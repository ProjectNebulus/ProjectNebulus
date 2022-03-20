from . import internal
from ....main.utils import private_endpoint
from .....static.python.spotify import get_song


@internal.route("/spotify-status", methods=["POST"])
@private_endpoint
def spotify_status():
    song = get_song()
    the_song = song[0]
    artist = song[1]
    art = song[2]
    string = ""
    if len(song) == 3:
        string = the_song + "-" + artist + "-" + art
    else:
        string = "You aren't listening to anything!"
    return string
