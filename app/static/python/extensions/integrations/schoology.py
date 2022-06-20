from datetime import datetime
from flask import session
import mechanize
import requests
from bs4 import BeautifulSoup
import schoolopy
from app.static.python.utils.colors import getColor
from app.static.python.mongodb import *


def scrapeSchoology():
    print("attempting login")

    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET",
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Max-Age": "3600",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
    }

    url = "https://app.schoology.com/login"
    driver = mechanize.Browser()
    driver.set_handle_robots(False)
    driver.open(url)

    for form in driver.forms():
        if form.attrs["id"] == "s-user-login-form":
            driver.form = form
            break

    user = create.generateSchoologyObject(session["id"])
    driver["mail"] = user.username
    driver["pass"] = user.password
    driver.submit()

    print("login successful")

    req = requests.get("https://app.schoology.com/home/course-dashboard", None, headers)
    soup = BeautifulSoup(req.content, "html.parser")

    return soup.prettify()


def get_schoology_emails():
    try:
        sc = read.getSchoologyAuth()

        messages = sc.get_inbox_messages()
        newMessages = []

        for message in messages:
            info = {}
            author = sc.get_user(message["author_id"])
            authorName = author["name_display"]
            authorPfp = author["picture_url"]
            authorEmail = author["primary_email"]
            authorSchool = sc.get_school(author["school_id"])["title"]
            authorColor = getColor(authorPfp)
            oldRecipients = message["recipient_ids"].split(",")
            recipients = []
            for recipient in oldRecipients:  # recipients:
                recipient = sc.get_user(recipient)
                school = sc.get_school(recipient["school_id"])["title"]
                color = getColor(recipient["picture_url"])
                recipients.append(
                    {
                        "name": recipient["name_display"],
                        "avatar": recipient["picture_url"],
                        "email": recipient["primary_email"],
                        "school": school,
                        "color": color,
                    }
                )

            author = {
                "name": authorName,
                "avatar": authorPfp,
                "email": authorEmail,
                "school": authorSchool,
                "color": authorColor,
            }
            info["subject"] = message["subject"]
            info["status"] = message["message_status"]
            thread = sc.get_message(message_id=message["id"])
            # print(thread)
            info["message"] = thread[-1]["message"]
            info["message"] = info["message"][:100] + "..." * (
                len(info["message"]) > 100
            )
            newThread = []
            for threadItem in thread:
                thread_author_id = threadItem["author_id"]
                thread_author = sc.get_user(thread_author_id)
                newThread.append(
                    {
                        "message": threadItem["message"],
                        "author": thread_author["name_display"],
                        "author_pic": thread_author["picture_url"],
                        "author_email": thread_author["primary_email"],
                    }
                )
            info["thread"] = newThread
            info["recipients"] = recipients
            info["author"] = author
            info["updated"] = datetime.fromtimestamp(int(message["last_updated"]))
            # print(temp)
            newMessages.append(info)

        newMessages = enumerate(newMessages)
    except:
        newMessages = enumerate([])
    return newMessages


def create_schoology(key, secret):
    sc = schoolopy.Schoology(schoolopy.Auth(key, secret))
    sc.limit = 100
    return sc


def create_schoology_auth(key, secret, auth):
    sc = schoolopy.Schoology(auth)
    sc.limit = 100
    return sc


def generate_auth(
    authorize,
    key,
    secret,
    domain,
    three_legged,
    request_token,
    request_token_secret,
    access_token,
    access_token_secret,
):
    auth = schoolopy.Auth(
        key,
        secret,
        domain=domain,
        three_legged=True,
        request_token=request_token,
        request_token_secret=request_token_secret,
        access_token=access_token,
        access_token_secret=access_token_secret,
    )
    if authorize:
        auth.authorize()
