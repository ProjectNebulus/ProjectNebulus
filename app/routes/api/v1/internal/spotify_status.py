from . import internal
from ....main.utils import private_endpoint
from .....static.python.spotify import get_song


@internal.route("/spotify-status", methods=["POST"])
def spotify_status():
    song = get_song()
    if len(song) == 8:
        name, artists2, album, explicit, image, playing, timestamp, total = song
        if explicit:
            explicit = "[Explicit]"
        else:
            explicit = ""
        artists = ""
        count = 0
        for i in artists2:
            artists += i
            count += 1
            if count != len(artists2):
                artists += ", "

        string = name + " • " + artists + " • " + album + " • " + str(explicit) + " • " \
                 + image + " • " + str(playing) + " • " + str(timestamp) + " • " + str(total)
    else:
        string = "You aren't listening to anything!"
    return string
