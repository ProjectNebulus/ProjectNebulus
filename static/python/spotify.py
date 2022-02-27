import sys

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from SwSpotify import spotify


def status():
    return get_song("")


def get_song():
    client_credentials_manager = SpotifyClientCredentials(
        client_id="b61065c28d774965b96027c3e2def9d9",
        client_secret="f0f01a4427ea4b48a9defabb46749311",
    )
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    try:
        currentsong = spotify.song()
        songartist = spotify.artist()

        print(f"Song Playing: {currentsong}\nArtist: {songartist}")

        if len(sys.argv) > 1:
            name = songartist.join(sys.argv[1:])
        else:
            name = songartist

        results = sp.search(q="artist:" + name, type="artist")
        items = results["artists"]["items"]
        if len(items) > 0:
            artist = items[0]
            print(
                artist["name"] + ": Artist Cover Image Link: ",
                artist["images"][0]["url"],
            )
            return (currentsong, songartist, artist["images"][0]["url"])
    except:
        print("Spotify is not running")
        return ()


def attemptsongart():
    client_credentials_manager = SpotifyClientCredentials(
        client_id="b61065c28d774965b96027c3e2def9d9",
        client_secret="f0f01a4427ea4b48a9defabb46749311",
    )
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    currentsong = spotify.song()
    songartist = spotify.artist()

    print(f"Song Playing: {currentsong}\nArtist: {songartist}")

    if len(sys.argv) > 1:
        name = currentsong.join(sys.argv[1:])
    else:
        name = currentsong

    results = sp.search(q="song:" + name, type="track")
    items = results["tracks"]["items"]
    if len(items) > 0:
        artist = items[0]
        print(artist["name"] + ": Song Cover Image Link: ", artist["images"][0]["url"])


# attemptsongart()
