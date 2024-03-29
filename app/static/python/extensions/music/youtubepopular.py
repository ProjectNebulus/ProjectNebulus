import os

import flask
import google.oauth2.credentials
import google_auth_oauthlib.flow
import requests
from flask import redirect, request, session
from googleapiclient.discovery import build

# -*- coding: utf-8 -*-

os.environ["OAUTHLIB_RELAX_TOKEN_SCOPE"] = "None"
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

# This variable specifies the name of a file that contains the OAuth 2.0
# information for this application, including its client_id and client_secret.
CLIENT_SECRETS_FILE = "../../credentials.json"

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
SCOPES = "https://www.googleapis.com/auth/youtube.readonly"
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"

app = flask.Flask(__name__)
# # Note: A secret key is included in the sample so that it works.
# # If you use this code in your application, replace this with a truly secret
# # key. See https://flask.palletsprojects.com/quickstart/#sessions.
app.secret_key = "REPLACE ME - this value is here as a placeholder."


@app.route("/youtube")
def gtest_api_request():
    if "credentials" not in flask.session:
        return flask.redirect("/youtube/authorize")
    try:
        # Load credentials from the session.
        credentials = google.oauth2.credentials.Credentials(
            **flask.session["credentials"]
        )

        youtube = build("youtube", "v3", credentials=credentials)

        # Call the Classroom API

        request = youtube.videos().list(chart="mostPopular")
        response = request.execute()
        # Save credentials back to session in case access token was refreshed.
        # ACTION ITEM: In a production app, you likely want to save these
        #              credentials in a persistent database instead.
        flask.session["credentials"] = credentials_to_dict(credentials)
    except:  # TokenExpired
        return flask.redirect("/youtube/authorize")
    request = youtube.videos().list(chart="mostPopular")
    response = request.execute()
    return str(response)
    # return flask.jsonify(courses)


@app.route("/youtube/authorize")
def authorize():
    # Create flow instance to manage the OAuth 2.0 Authorization Grant Flow steps.
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES
    )

    # The URI created here must exactly match one of the authorized redirect URIs
    # for the OAuth 2.0 client, which you configured in the API Console. If this
    # value doesn't match an authorized URI, you will get a 'redirect_uri_mismatch'
    # error.
    if "local" not in request.root_url:
        flow.redirect_uri = (
            request.root_url.replace("http", "https") + "youtube/oauth2callback"
        )
    else:
        flow.redirect_uri = request.root_url + "youtube/oauth2callback"
    print(request.root_url.replace("http", "https") + "youtube/oauth2callback")
    authorization_url, state = flow.authorization_url(
        # Enable offline access so that you can refresh an access token without
        # re-prompting the user for permission. Recommended for web server apps.
        access_type="offline",
        # Enable incremental authorization. Recommended as a best practice.
        include_granted_scopes="true",
    )

    # Store the state so the callback can verify the auth server response.
    session["state"] = state

    return redirect(authorization_url)


@app.route("/youtube/oauth2callback")
def oauth2callback():
    # Specify the state when creating the flow in the callback so that it can
    # verified in the authorization server response.
    state = flask.session["state"]

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES, state=state
    )
    # flow.redirect_uri = flask.url_for('youtube/oauth2callback', _external=True)
    flow.redirect_uri = flask.url_for("oauth2callback", _external=True)
    print(flow.redirect_uri)
    # Use the authorization server's response to fetch the OAuth 2.0 tokens.
    authorization_response = flask.request.url
    flow.fetch_token(authorization_response=authorization_response)

    # Store credentials in the session.
    # ACTION ITEM: In a production app, you likely want to save these
    #              credentials in a persistent database instead.
    credentials = flow.credentials
    flask.session["credentials"] = credentials_to_dict(credentials)

    # return flask.redirect(flask.url_for("main_blueprint.g_classroom_auth"))
    return flask.redirect(flask.url_for("gtest_api_request"))


@app.route("/youtube/revoke")
def revoke():
    if "credentials" not in flask.session:
        return (
            'You need to <a href="/authorize">authorize</a> before '
            + "testing the code to revoke credentials."
        )

    credentials = google.oauth2.credentials.Credentials(**flask.session["credentials"])

    revoke = requests.post(
        "https://oauth2.googleapis.com/revoke",
        params={"token": credentials.token},
        headers={"content-type": "application/x-www-form-urlencoded"},
    )

    status_code = getattr(revoke, "status_code")
    if status_code == 200:
        return redirect("/settings")
    else:
        return redirect("/settings")


@app.route("/youtube/clear")
def clear_credentials():
    if "credentials" in flask.session:
        del flask.session["credentials"]
    return "Credentials have been cleared.<br><br>" + print_index_table()


def credentials_to_dict(credentials):
    return {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes": credentials.scopes,
    }


def print_index_table():
    return (
        "<table>"
        + '<tr><td><a href="/test">Test an API request</a></td>'
        + "<td>Submit an API request and see a formatted JSON response. "
        + "    Go through the authorization flow if there are no stored "
        + "    credentials for the user.</td></tr>"
        + '<tr><td><a href="/authorize">Test the auth flow directly</a></td>'
        + "<td>Go directly to the authorization flow. If there are stored "
        + "    credentials, you still might not be prompted to reauthorize "
        + "    the application.</td></tr>"
        + '<tr><td><a href="/revoke">Revoke current credentials</a></td>'
        + "<td>Revoke the access token associated with the current user "
        + "    session. After revoking credentials, if you go to the test "
        + "    page, you should see an <code>invalid_grant</code> error."
        + "</td></tr>"
        + '<tr><td><a href="/clear">Clear Flask session credentials</a></td>'
        + "<td>Clear the access token currently stored in the user session. "
        + '    After clearing the token, if you <a href="/test">test the '
        + "    API request</a> again, you should go back to the auth flow."
        + "</td></tr></table>"
    )


if __name__ == "__main__":
    app.run("localhost", 8080, debug=True)
