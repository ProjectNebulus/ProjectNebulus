ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}


def dl_youtube(query):
    import youtube_dl
    from youtube_search import YoutubeSearch

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    location = "./static/video/"
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([f"ytsearch1:{query}"])
    return location + query + ".mp3"


def search_yt(query):
    import urllib.request
    import re
    search_keyword = query
    while ' ' in search_keyword:
        for i in range(0, len(search_keyword)):
            if ' ' == search_keyword[i]:
                search_keyword = search_keyword[0:i] + '%20' + search_keyword[
                                                               i + 1:len(search_keyword)]
                break

    html = urllib.request.urlopen(
        "https://www.youtube.com/results?search_query=" + str(search_keyword.encode('utf-8')))

    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())

    return video_ids[0]
