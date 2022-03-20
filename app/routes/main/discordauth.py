import flask_discord
from flask_discord import DiscordOAuth2Session, requires_authorization, Unauthorized
from flask import current_app
from flask import render_template, redirect, session
import discord

from . import main_blueprint


@main_blueprint.route("/discord")
def discord_auth():
    thediscord = None
    with current_app.app_context():
        current_app.config["DISCORD_CLIENT_ID"] = 826815572472758333  # Discord client ID.
        current_app.config["DISCORD_CLIENT_SECRET"] = "UmFqaDEbgPdtLAjw_ObAbqNWuNquIZTv"  # Discord client secret.
        current_app.config["DISCORD_REDIRECT_URI"] = "https://camphalfblooddiscord.ga/recieve"

        thediscord = DiscordOAuth2Session()

    return thediscord.create_session()
