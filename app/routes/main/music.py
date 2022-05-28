import json

from flask import render_template, request

from . import main_blueprint
from .utils import logged_in


@main_blueprint.route("/music", methods=["GET"])
@logged_in
def music():
    return render_template("music.html")


@main_blueprint.route('/music', methods=['POST'])
@logged_in
def music_post():

    text = request.form['search']
    import requests

    CLIENT_ID = '846095b9ce934b0da3e0aaf3adbf600c'
    CLIENT_SECRET = '1d79c77cee124d8f8e20b16f720d65e8'
    AUTH_URL = 'https://accounts.spotify.com/api/token'
    # POST
    auth_response = requests.post(
        AUTH_URL, {
            'grant_type': 'client_credentials',
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        })

    # convert the response to JSON
    auth_response_data = auth_response.json()

    # save the access token
    access_token = auth_response_data['access_token']

    artist_info = requests.get(
        f'https://api.spotify.com/v1/search?q={text}&type=track',
        headers={
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }).json()
    #print(artist_info)
    print(access_token)

    spotify_arr = []
    with open('app/static/json/cache.json', 'r') as file:
        file = json.load(file)
    for i in range(0, len(artist_info['tracks']['items'])):
        if i < 10:
            mydict = {}
            mydict['image'] = str(
                artist_info['tracks']['items'][i]['album']['images'][0]['url'])
            mydict['author'] = (artist_info['tracks']['items'][i]['album']
            ['artists'][0]['name'])
            mydict['author_url'] = artist_info['tracks']['items'][i]['album'][
                'artists'][0]['external_urls']["spotify"]
            mydict['album'] = (
                artist_info['tracks']['items'][i]['album']['name'])
            mydict['explicit'] = artist_info['tracks']['items'][i]['explicit']
            mydict['name'] = (artist_info['tracks']['items'][i]['name'])
            mydict['preview'] = (
                artist_info['tracks']['items'][i]['preview_url'])
            mydict['link'] = (
                artist_info['tracks']['items'][i]['external_urls']['spotify'])
            mydict['code'] = mydict['link'][31:len(mydict['link'])]
            mydict['uri'] = (artist_info['tracks']['items'][i]['uri'])
            spotify_arr.insert(0, mydict)
            file.append(mydict)
    processed_text = text.upper()
    with open('app/static/json/cache.json', 'w') as out:
        file = json.dump(file, out, indent=4)
    import urllib.request
    import re
    search_keyword = processed_text
    while ' ' in search_keyword:
        for i in range(0, len(search_keyword)):
            if ' ' == search_keyword[i]:
                search_keyword = search_keyword[0:i] + '%20' + search_keyword[
                                                               i + 1:len(search_keyword)]
                break

    html = urllib.request.urlopen(
        "https://www.youtube.com/results?search_query=" + search_keyword)

    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())

    def find_data(link, param):
        #author_name
        #author_url
        #thumbnail_url
        #title
        import urllib.request
        import json
        import urllib
        import pprint

        #change to yours VideoID or change url inparams
        VideoID = link

        params = {
            "format": "json",
            "url": "https://www.youtube.com/watch?v={}".format(VideoID)
        }
        url = "https://www.youtube.com/oembed"
        query_string = urllib.parse.urlencode(params)
        url = url + "?" + query_string

        with urllib.request.urlopen(url) as response:
            response_text = response.read()
            data = json.loads(response_text.decode())
            #pprint.pprint(data)
            return data[param]

    if len(video_ids) == 0 and len(spotify_arr) == 0:
        return render_template('musicresults.html', noresults=True)

    else:
        mylist = []
        for i in range(0, len(video_ids)):
            if i < 10:
                #author_name
                #author_url
                #thumbnail_url
                #title

                try:
                    my_dict = {"id": video_ids[i]}
                    my_dict["author_name"] = find_data(video_ids[i], "author_name")
                    my_dict["author_url"] = find_data(video_ids[i], "author_url")
                    my_dict["thumbnail_url"] = find_data(video_ids[i],"thumbnail_url")
                    my_dict["title"] = find_data(video_ids[i], "title")
                    mylist.append(my_dict)
                except:
                    continue

            else:
                break

    return render_template('musicresults.html',
                           noresults=False,
                           mylist=mylist,
                           spotify_arr=spotify_arr)


@main_blueprint.route('/play/spotify/<smth>')
@logged_in
def music_spotify(smth):
    extra = ''
    with open('app/static/json/cache.json', 'r') as file:
        file = json.load(file)
    for i in file:
        if i['code'] == smth:
            return render_template('musictrack.html', i=i)


@main_blueprint.route('/play/<id_>')
@logged_in
def music_video(id_:str):
    def find_data(link, param):
        #author_name
        #author_url
        #thumbnail_url
        #title
        import urllib.request
        import json
        import urllib
        import pprint
        #change to yours VideoID or change url inparams
        VideoID = link
        params = {"format": "json", "url": "https://www.youtube.com/watch?v=%s" % VideoID}
        url = "https://www.youtube.com/oembed"
        query_string = urllib.parse.urlencode(params)
        url = url + "?" + query_string
        with urllib.request.urlopen(url) as response:
            response_text = response.read()
            data = json.loads(response_text.decode())
            pprint.pprint(data)
            return data[param]

    youtube = f'https://www.youtube.com/watch?v={id_}'
    link = f'https://nebulus.ml/play/{id_}'
    author = find_data(id_,'author_name')
    author_url = find_data(id_,'author_url')
    sub = author_url+'?sub_confirmation=1'
    thumbnail_url = find_data(id_,'thumbnail_url')
    title = find_data(id_,'title')
    content = f'Listen to {title} by {author} on Nebulus!'
    return render_template('musicvideo.html',author=author,author_url=author_url,thumbnail_url=thumbnail_url,title=title,id=id_,content=content,youtube=youtube,sub=sub,link=link)
