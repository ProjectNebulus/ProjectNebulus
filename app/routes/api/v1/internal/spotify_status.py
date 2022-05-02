from . import internal
from ....main.utils import private_endpoint
from .....static.python.spotify import get_song

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
            playing = '<i class="material-icons">play_circle</i>'
        else:
            playing = '<i class="material-icons">pause_circle</i>'
        string = name + " • " + artists + " • " + album + " • " + str(explicit) + " • " \
                 + image + " • " + str(playing) + " • " + str(timestamp) + " • " + str(total) \
                 + " • " + str(ratio)
    else:
        string = "You aren't listening to anything!"
    return string
