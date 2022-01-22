from SwSpotify import spotify
# import pyautogui
import os


def status():
    return get_song("")


def get_song(old_song):
    try:
        current_song = spotify.song()
        current_artist = spotify.artist()
    except:
        current_song = "no_song_is_playing_right_now"
        current_artist = ""

    return [current_song, current_artist]
