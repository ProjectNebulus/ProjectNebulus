from ...routes.main.spotify import GET_currently_playing


def get_song():
    answer = GET_currently_playing()
    if answer == "No":
        return []
    return answer