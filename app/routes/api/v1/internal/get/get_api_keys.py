from flask import session, request

from app.static.python.mongodb import read
from .. import internal


@internal.route("/get/api-keys/schoology", methods=["GET"])
def schoology_api_keys():
    account_name = request.args.get("name")
    schoology = read.get_schoology(id=session["id"])

    if not schoology:
        return "No schoology found", 422

    account = None
    for account in schoology:
        if account.name == account_name:
            break

    key = account.api_key
    secret = account.api_secret

    if request.args.get("hide"):
        secret = "*" * len(secret)

    if not account or not account.api_key or not account.api_secret:
        return "No schoology account with the specified name found", 422

    return "\n".join((key, secret)), 200
