# Import the Canvas class
from canvasapi import Canvas

# Canvas API URL
# API_URL = "https://example.com"
API_URL = "https://canvas.instructure.com"
# Canvas API key
# API_KEY = "p@$$w0rd"
API_KEY = "7~rxTmMaJBs8VPA6i2BDcYgbX4N9MvYV2hF5wfvjTpSDxGLrbxZpmQsdOg56JLXCy2"

# Initialize a new Canvas object
canvas = Canvas(API_URL, API_KEY)

token = "7~rxTmMaJBs8VPA6i2BDcYgbX4N9MvYV2hF5wfvjTpSDxGLrbxZpmQsdOg56JLXCy2"
link = "https://canvas.instructure.com/login/oauth2/auth?client_id=7~rxTmMaJBs8VPA6i2BDcYgbX4N9MvYV2hF5wfvjTpSDxGLrbxZpmQsdOg56JLXCy2&response_type=code&redirect_uri=https://example.com/oauth_complete"

# account = canvas.get_user(user="self")
account = canvas.get_user(25669154)
# account = canvas.get_account(25669154)
# account = canvas.get_user(26081494)
courses = account.get_courses()

logins = account.get_user_logins()

for login in logins:
    print(login)

for course in courses:
    print(course)
    assignments = course.get_assignments()
    for assignment in assignments:
        print("    " + str(assignment))
