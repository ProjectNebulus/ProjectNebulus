import requests
from flask import redirect, render_template, request, session

from app.static.python.mongodb import update
from . import main_blueprint


def get_auth():
    client_id = "a5443a5dffe717b56bf2"
    return f"https://github.com/login/oauth/authorize?client_id={client_id}"


def get_access_token(request_token: str) -> str:
    CLIENT_ID = "a5443a5dffe717b56bf2"
    CLIENT_SECRET = "8c895931234e1d44734b29b9e966d8917cda454e"

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


@main_blueprint.route("/github")
def github():
    return redirect(get_auth())


@main_blueprint.route("/github/auth")
def github_callback():
    code = request.args.get("code")
    print(code)
    token = get_access_token(code)
    update.githubLogin(
        session["id"],
        {
            "token": token,
            "username": get_user_data(token)["login"],
            "avatar": get_user_data(token)["avatar_url"],
        },
    )
    return render_template(
        "user/connections/connectGithub.html",
        username=get_user_data(token)["login"],
        avatar=get_user_data(token)["avatar_url"],
    )


@main_blueprint.route("/github/repos")
def get_repos():
    github_repos = get_user_repos(session["github"])
    repos = []
    for repo in github_repos:
        repos.append([repo["full_name"], (repo["visibility"] != "public")])
    string = ""
    for repo in repos:
        symbol = ""
        if repo[1]:
            symbol = "<i class='material-icons'>lock</i>"
        string += (
            "<p>"
            + """
		<img src="https://cdn-icons-png.flaticon.com/512/25/25231.png" style="
    filter: invert(1);
    height: 30px;
    vertical-align: middle;
    margin: 10px;
">
	"""
            + repo[0]
            + symbol
            + """<button style="
    margin: 20px;
    font-weight: 600;
    border: none;
    font-family: 'Montserrat';
    padding: 10px 20px;
    border-radius: 10px;
    background: deepskyblue;
">Import</button>"""
            + "</p>"
        )
    return string
