from flask import Flask, redirect, request, session, url_for
import google.oauth2.credentials
import google_auth_oauthlib.flow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

app = Flask(__name__)
app.secret_key = 'asdfghjkl'


@app.route("/")
def main():
    if "state" in request.args:
        state = session['state']
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            'client_secret.json',
            scopes=['https://www.googleapis.com/auth/drive.metadata.readonly'],
            state=state)
        flow.redirect_uri = url_for('oauth2callback', _external=True)

        authorization_response = request.url
        flow.fetch_token(authorization_response=authorization_response)

        # Store the credentials in the session.
        # ACTION ITEM for developers:
        #     Store user's access and refresh tokens in your data store if
        #     incorporating this code into your real app.
        credentials = flow.credentials
        session['credentials'] = {
            'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}
        from googleapiclient.discovery import build

        drive = build('drive', 'v2', credentials=credentials)
        files = drive.files().list().execute()
        # return str(request.args)
        return str(files)
    # Use the client_secret.json file to identify the application requesting
    # authorization. The client ID (from that file) and access scopes are required.
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        'credentials.json',
        scopes=['https://www.googleapis.com/auth/drive.metadata.readonly',
                'https://www.googleapis.com/auth/classroom.courses.readonly',
                'https://www.googleapis.com/auth/classroom.rosters.readonly',
                'https://www.googleapis.com/auth/classroom.coursework.me',
                'https://www.googleapis.com/auth/classroom.coursework.me.readonly',
                'https://www.googleapis.com/auth/classroom.coursework.students',
                'https://www.googleapis.com/auth/classroom.coursework.students.readonly',
                'https://www.googleapis.com/auth/classroom.announcements',
                'https://www.googleapis.com/auth/classroom.announcements.readonly',
                'https://www.googleapis.com/auth/classroom.guardianlinks.students.readonly',
                'https://www.googleapis.com/auth/classroom.guardianlinks.me.readonly',
                'https://www.googleapis.com/auth/classroom.push-notifications']
    )

    # Indicate where the API server will redirect the user after the user completes
    # the authorization flow. The redirect URI is required. The value must exactly
    # match one of the authorized redirect URIs for the OAuth 2.0 client, which you
    # configured in the API Console. If this value doesn't match an authorized URI,
    # you will get a 'redirect_uri_mismatch' error.
    flow.redirect_uri = 'http://localhost:8080'

    # Generate URL for request to Google's OAuth 2.0 server.
    # Use kwargs to set optional request parameters.
    authorization_url, state = flow.authorization_url(
        # Enable offline access so that you can refresh an access token without
        # re-prompting the user for permission. Recommended for web server apps.
        access_type='offline',
        # Enable incremental authorization. Recommended as a best practice.
        include_granted_scopes='true')

    print(authorization_url)
    print(state)
    session["state"] = state
    return redirect(authorization_url)


if __name__ == "__main__":
    print("Started running on http://localhost:8080")
    app.run(host="localhost", port=8080)
