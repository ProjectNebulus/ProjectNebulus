import json

from flask import Flask, redirect, render_template, request, session
from flask_discord import DiscordOAuth2Session

from . import main_blueprint

app = Flask(__name__)
app.config["DISCORD_CLIENT_ID"] = 955153343020429343  # Discord client ID.
app.config[
    "DISCORD_CLIENT_SECRET"
] = "6ApEyUtWUsp1SwuXlrRn3e_lNB6IqfSO"  # Discord client secret.
app.config["DISCORD_REDIRECT_URI"] = "null"


def generate_redirect(url):
    if "nebulus" in url:
        if "https" not in url:
            return url.replace("http", "https") + "discord/receive"
    return url + "discord/receive"


def exchange_code(code, url):
    data = {
        "client_id": 955153343020429343,
        "client_secret": "6ApEyUtWUsp1SwuXlrRn3e_lNB6IqfSO",
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": generate_redirect(url),
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    r = requests.post(
        "https://discord.com/api/v8/oauth2/token",
        data=data,
        headers=headers,
        verify=False,
    )
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
    url = f"{baseUrl}/{endpoint}"
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
    app.config["DISCORD_REDIRECT_URI"] = generate_redirect(request.root_url)
    discordAuth = DiscordOAuth2Session(app)

    return discordAuth.create_session()


@main_blueprint.route("/discord/receive")
def recieve():
    if "code" in request.args:
        try:
            code = request.args["code"]
            data = exchange_code(code, request.root_url)
            access_token = data["access_token"]
            data = getMe(access_token)

            avatar_link = (
                f"https://cdn.discordapp.com/avatars/{data['id']}/{data['avatar']}.png"
            )

            user = f"{data['username']}#{data['discriminator']}"

            data = [user, int(data["id"]), avatar_link]
            session["discord_code"] = code
            session["discord_access_token"] = access_token
            session["discord_avatar"] = avatar_link
            session["discord_user"] = user
            session["discord_id"] = data[1]

            return render_template("user/connections/connectDiscord.html", data=data)

        except Exception as e:
            print(e)

            return redirect("/discord")

    else:
        return redirect("/discord")
    resp = flask.make_response(redirect("/"))
    resp.set_cookie("login", str(data[0]))
    resp.set_cookie("id", str(data[1]))
    resp.set_cookie("avatar", str(data[2]))
    return resp


@main_blueprint.route("/github")
def github():
    return redirect(get_auth())


import requests


def get_auth():
    client_id = "a5443a5dffe717b56bf2"
    return f"https://github.com/login/oauth/authorize?client_id={client_id}"


def get_access_token(request_token: str) -> str:
    CLIENT_ID = "00526a398682e4475ba1"
    CLIENT_SECRET = "3b583a946d881ae85d6b187c3096ed98debe0343"

    url = f"https://github.com/login/oauth/access_token?client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}&code={request_token}"
    headers = {"accept": "application/json"}

    res = requests.post(url, headers=headers)

    data = res.json()
    print(data)
    access_token = data["access_token"]

    return access_token


def get_user_data(access_token: str) -> dict:
    if not access_token:
        raise ValueError("The request token has to be supplied!")
    if not isinstance(access_token, str):
        raise ValueError("The request token has to be a string!")

    access_token = "token " + access_token
    url = "https://api.github.com/user"
    headers = {"Authorization": access_token}

    resp = requests.get(url=url, headers=headers)

    userData = resp.json()

    return userData


def get_user_repos(access_token: str):
    if not access_token:
        raise ValueError("The request token has to be supplied!")
    if not isinstance(access_token, str):
        raise ValueError("The request token has to be a string!")
    access_token = "token " + access_token
    url = "https://api.github.com/user"
    headers = {"Authorization": access_token}
    resp = requests.get(url=url, headers=headers)
    userData = resp.json()
    username = userData["login"]
    url = f"https://api.github.com/users/{username}/repos"
    headers = {"Authorization": access_token}
    resp = requests.get(url=url, headers=headers)
    repoData = resp.json()
    url = f"https://api.github.com/users/{username}/orgs"
    headers = {"Authorization": access_token}
    resp = requests.get(url=url, headers=headers)
    orgData = resp.json()
    for org in orgData:
        # url = f"https://api.github.com/users/{org['login']}/orgs"
        url = f"https://api.github.com/users/{org['login']}/repos"
        headers = {"Authorization": access_token}
        resp = requests.get(url=url, headers=headers)
        org_subData = resp.json()
        repoData += org_subData
    # print(orgData)
    return repoData
