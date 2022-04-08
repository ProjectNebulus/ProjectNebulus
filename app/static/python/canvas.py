def connectCanvas(url, key):
    try:
        from canvasapi import Canvas
        API_URL = url
        API_KEY = key
        canvas = Canvas(API_URL, API_KEY)
        account = canvas.get_user(user="self")
        return account
    except:
        return False


def getCourses(url, key):
    account = connectCanvas(url, key)
    courses = account.get_courses()
    return courses
