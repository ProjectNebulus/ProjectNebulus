import flask_discord
from flask_discord import DiscordOAuth2Session, requires_authorization, Unauthorized
from flask import current_app
from flask import Flask, request, redirect
import discord
import requests
from . import main_blueprint
import json

app = Flask(__name__)
app.config["DISCORD_CLIENT_ID"] = 955153343020429343  # Discord client ID.
app.config["DISCORD_CLIENT_SECRET"] = "6ApEyUtWUsp1SwuXlrRn3e_lNB6IqfSO"  # Discord client secret.
app.config["DISCORD_REDIRECT_URI"] = "http://localhost:8080/discord/receive"


def exchange_code(code):
    data = {
        'client_id': 826815572472758333,
        'client_secret': "UmFqaDEbgPdtLAjw_ObAbqNWuNquIZTv",
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': "https://camphalfblooddiscord.ga/recieve"
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    r = requests.post('https://discord.com/api/v8/oauth2/token', data=data, headers=headers)
    # r.raise_for_status()
    return r.json()


global baseUrl
baseUrl = "https://discordapp.com/api"


def getHeaders(access_token):
    return {
        "Authorization": "{} {}".format("Bearer", access_token),
        # "user-agent" : "DiscordBackup/0.0.1"
    }


def getRequest(access_token, endpoint, asJson=True, additional=None):
    url = "{}/{}".format(baseUrl, endpoint)
    req = requests.get(url, headers=getHeaders(access_token))

    if asJson:
        return json.loads(req.text)
    else:
        return req.text


def getMe(access_token):  # this works
    endpoint = "users/@me"
    return getRequest(access_token, endpoint)


@main_blueprint.route("/discord")
def discord_auth():
    app.config["DISCORD_REDIRECT_URI"] = request.root_url + "discord/recieve"
    print(request.root_url + "discord/receive")
    thediscord = DiscordOAuth2Session(app)

    return thediscord.create_session()


@main_blueprint.route('/discord/receive')
def recieve():
    import json
    if "code" in request.args:
        try:
            code = request.args["code"]

            data = exchange_code(code)

            access_token = data['access_token']

            data = getMe(access_token)

            avatar_link = f"https://cdn.discordapp.com/avatars/{data['id']}/{data['avatar']}.png"

            user = f"{data['username']}#{data['discriminator']}"

            data = [user, int(data['id']), avatar_link]
            return data



        except Exception as e:
            print(e)

            return redirect("/discord")


    else:
        return redirect("/discord")
    resp = flask.make_response(redirect('/'))
    resp.set_cookie('login', str(data[0]))
    resp.set_cookie('id', str(data[1]))
    resp.set_cookie('avatar', str(data[2]))
    return resp
