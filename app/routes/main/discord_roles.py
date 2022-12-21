import json

import datetime
import requests
from flask import Flask, redirect, render_template, request, session
from flask_discord import DiscordOAuth2Session

from app.static.python.mongodb import update
from . import main_blueprint, logged_in
from ...static.python.mongodb.read import getText, find_user, get_user_courses

app = Flask(__name__)
app.config["DISCORD_CLIENT_ID"] = 992107195003043841  # Discord client ID.
app.config[
    "DISCORD_CLIENT_SECRET"
] = "lxvcD2qBjLzeS2rERdvmm26no3IAc4KV"  # Discord client secret.
app.config["DISCORD_REDIRECT_URI"] = "null"


def generate_redirect(url):
    if "nebulus" in url:
        if "https" not in url:
            return url.replace("http", "https") + "discord-roles/receive"
    return url + "discord-roles/receive"


def exchange_code(code, url):
    data = {
        "client_id": 992107195003043841,
        "client_secret": "lxvcD2qBjLzeS2rERdvmm26no3IAc4KV",
        "grant_type": "authorization_code",
        "code": code,
        "scope": "role_connections.write identify",
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


@main_blueprint.route("/discord-roles")
@logged_in
def roles_discord_auth():
    app.config["DISCORD_REDIRECT_URI"] = generate_redirect(request.root_url)
    discordAuth = DiscordOAuth2Session(app)

    return discordAuth.create_session(scope=["role_connections.write", "identify"])

def push_metadata(access_token):
    url = "https://discord.com/api/v10/users/@me/applications/992107195003043841/role-connection"
    user = find_user(id=session["id"])
    course_amount = len(get_user_courses(session["id"]))
    data = {
        "platform_name": user.username,
        "metadata": {
            "isstaff": 1 if user.is_staff else 0,
            "earlysupporter": 1 if user.created_at < datetime.datetime(2022, 12, 18, 0, 0, 0) else 0,
            "courseamount": course_amount,
            "date_created": user.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "schoology_user": 1 if user.schoology else 0,
        }
    }

    requests.put(url, headers={"Content-Type": "application/json", "Authorization": f'Bearer {access_token}'}, data=json.dumps(data))




@main_blueprint.route("/discord-roles/receive")
def roles_recieve():
    if "code" in request.args:
        try:
            code = request.args["code"]
            data = exchange_code(code, request.root_url)
            access_token = data["access_token"]
            data = getMe(access_token)
            push_metadata(access_token)

            avatar_link = (
                f"https://cdn.discordapp.com/avatars/{data['id']}/{data['avatar']}.png"
            )

            user = f"{data['username']}#{data['discriminator']}"

            data = [user, int(data["id"]), avatar_link]
            discord_dict = {
                "discord_code": code,
                "discord_id": data[1],
                "discord_user": str(user),
                "discord_avatar": avatar_link,
                "discord_access_token": access_token,
            }
            update.discordLogin(session["id"], discord_dict)

            return render_template("user/connections/connectDiscord.html", data=data, translate = getText)

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
