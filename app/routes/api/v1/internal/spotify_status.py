from . import internal
from ....main.utils import private_endpoint
from .....static.python.spotify import get_song
from .....routes.main.spotify import shuffle_spotify, shuffle2_spotify, loop_spotify, \
    loop1_spotify, loop2_spotify, pause_spotify, next_spotify, prev_spotify, resume_spotify

def convert(secs):
    part1 = str(secs//60)
    part2 = str(secs % 60)
    if len(part2) == 1:
        part2 = "0"+part2
    return f"{part1}:{part2}"

@internal.route("/spotify-status", methods=["POST"])
def spotify_status():
    song = get_song()
    if song[0] == 1:
        return "1" #Spotify Not Detected
    if song[0] == 2:
        return "2" #Spotify Isn't Connected
    if len(song) == 8:
        name, artists2, album, explicit, image, playing, timestamp, total = song
        if explicit:
            explicit = '<i class="material-icons">explicit</i>'
        else:
            explicit = ""
        artists = ""
        count = 0
        for i in artists2:
            artists += i
            count += 1
            if count != len(artists2):
                artists += ", "
        ratio = round(timestamp/total*100)
        timestamp = convert(timestamp)
        total = convert(total)
        if not playing:
            playing = '<i onclick="sendRQ(\'/api/v1/internal/spotify/resume\')" style="font-size:48px !important;" ' \
                      'class="material-icons">play_circle</i> '
        else:
            playing = '<i onclick="sendRQ(\'/api/v1/internal/spotify/pause\')" style="font-size:48px !important;" ' \
                      'class="material-icons">pause_circle</i> '
        string = name + " • " + artists + " • " + album + " • " + str(explicit) + " • " \
                 + image + " • " + str(playing) + " • " + str(timestamp) + " • " + str(total) \
                 + " • " + str(ratio)
    else:
        string = "You aren't listening to anything!"
    return string
@internal.route("/spotify/skip-f", methods=["POST"])
def spotifyskipf():
    next_spotify()
    return "Success"
@internal.route("/spotify/skip-b", methods=["POST"])
def spotifyskipb():
    prev_spotify()
    return "Success"
@internal.route("/spotify/shuffle", methods=["POST"])
def spotifyshuffle():
    shuffle_spotify()
    return "Success"
@internal.route("/spotify/stopshuffle", methods=["POST"])
def spotifystopshuffle():
    shuffle2_spotify()
    return "Success"
@internal.route("/spotify/loop_small", methods=["POST"])
def spotifyloop():
    loop_spotify()
    return "Success"
@internal.route("/spotify/loop_big", methods=["POST"])
def spotifyloop1():
    loop1_spotify()
    return "Success"
@internal.route("/spotify/loop_big", methods=["POST"])
def spotifystoploop():
    loop2_spotify()
    return "Success"
@internal.route("/spotify/pause", methods=["POST"])
def spotifypause():
    pause_spotify()
    return "Success"

@internal.route("/spotify/resume", methods=["POST"])
def spotifyresume():
    resume_spotify()
    return "Success"