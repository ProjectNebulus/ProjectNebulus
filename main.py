"""
App entrypoint.
"""
import os

from waitress import serve

from app.routes import init_app

app = init_app()
print(app.url_map)
app.secret_key = os.getenv("MONGOPASS")
regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"

from app.static.python.mongodb import create

# create.createAnnouncement({"course":"1497078952970289156", "title":"English 7",
#                            "content" : "Someone left their laptop in Rm. 344!  It has a black and red case, and it is an Apple.  If you don't come get it in the next 10 minutes, I will put it in our lost and found in Rm. 233.  I will be in Rm. 234 until 4:30PM to open the room for you.",
#                            "author_pic" : "https://asset-cdn.schoology.com/users/95200861/profile-image/profile_sm?1596748684",
#                                                                                                                            "author" : "Ms. Nagami",
#                                                "likes": 3,
#                                 "imported_from" : "Schoology"})
# create.createAnnouncement({"course":"1497078952970289156", "title":"English 7",
#                            "content" : "Hi, Students.  Recorders: Don't worry about uploading the rough draft to Turnitin.com.  I'm having an issue with my account; I will try to get it resolved before the final draft is due.",
#                            "author_pic" : "https://asset-cdn.schoology.com/users/95200861/profile-image/profile_sm?1596748684",
#                            "author" : "Ms. Nagami",
#                            "likes": 0,
#                            "imported_from" : "Schoology"})
# create.createAnnouncement({"course":"1497078952970289156", "title":"English 7",
#                            "content" : "Also, please be sure to make your Zoom name your first and last name.",
#                            "author_pic" : "https://asset-cdn.schoology.com/users/95200861/profile-image/profile_sm?1596748684",
#                            "author" : "Ms. Nagami",
#                            "likes": 0,
#                            "imported_from" : "Schoology"})
# app.register_blueprint(error_blueprint)
if __name__ == "__main__":
    print("Started running on http://localhost:8080")
    serve(app=app, host="0.0.0.0", port=8080)
