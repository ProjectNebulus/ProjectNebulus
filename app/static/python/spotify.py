from ...routes.main.spotify import GET_currently_playing


def get_song():
    answer = GET_currently_playing()
    if answer == 1:
        return [1]
    elif answer == 2:
        return [2]
    return answer