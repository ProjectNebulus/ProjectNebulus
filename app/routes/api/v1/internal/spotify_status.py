from .__init__ import internal
from .private_endpoint import private_endpoint
from .....static.python.spotify import get_song


@internal.route("/spotify-status", methods=["POST"])
@private_endpoint
def spotify_status():
    song = get_song()
    string = ""
    if len(song) == 3:
        string = a[0] + " - " + a[1]
    else:
        string = "You aren't listening to anything!"
    return string
