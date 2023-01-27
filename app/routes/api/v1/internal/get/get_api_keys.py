from flask import session, request

from app.static.python.mongodb import read
from .. import internal


@internal.route("/get/api-keys/schoology", methods=["GET"])
def schoology_api_keys():
    print("Reached here")

    account_name = request.args.get("name")
    print("Reached here")

    schoology = read.get_schoology(id=session["id"])
    print("Reached here")

    if not schoology:
        print("Reached there")
        return "No schoology found", 422

    account = None
    for account in schoology:
        if account.name == account_name:
            break

    print("Reached here")
    if not account:
        print("Reached there")
        return "No account with the specified name found", 422

    print("Reached here")

    return "\n".join((account.api_key, account.api_secret)), 200
