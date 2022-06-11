"""
App entrypoint.
"""
import os
import platform

from waitress import serve
from app.static.python.mongodb import delete
from app.static.python.classes.Announcement import Announcement

from app.routes import init_app

app = init_app()
app.secret_key = os.getenv("MONGOPASS")
regex = r"\b[A-Za-z0-9._%+]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
"""
IMPORTANT!
IF YOU HAVE CHANGED A FIELD IN ONE OF THE MONGODB OBJECTS, YOU MUST UPDATE THE EXISTING DOCUMENTS!
Do that by calling this function


cls is the class of the object, field is the field that was changed, value is the the default value
"""
"https://files-cdn.schoology.com/5bc1ce116299156188bd2f3d8f15302f?content-type=application%2Fpdf&content-disposition=attachment%3B%2Bfilename%3D%2213.0_Week13_Schedule_corrected.pdf%22&Expires=1651983347&Signature=QXg64qTO4T5moj61eo21PDJFkCFfs-DUjMNKgsEvkHVPQfddCEyaBMww3Qii6Z~wXQLuDK-YOFFkvU~KS7AfNpreYuhkRuWTYIT3qQPPupzl-VEJ4kV8w4srhCUeQdj5lGz~Y5uwekOFTL8ehhNop7z~32Q~8IZpJKGYd~z2JULeyXbOE0JOsyeGsYcWffSiel1xjqu08coHCNJ-MH7z1hS~PRy6HygWQaz4TJBD~LVQyNxINxFGK-MVTQKRNKUmTTmWF699SDhakG9k04tPOwHYILakSwlAsOpBozUkr3wfC6MLkSFzvMFgyLLJCPPSEy7OWJHYLZ28E0TQxcexzw__&Key-Pair-Id=APKAJ6LPJQLQJLURLVDQ"

debug = False
if __name__ == "__main__":
    if platform.system().lower() == "linux":
        debug = False
        port = 80
        host = "0.0.0.0"
    else:  # macos (darwin) or windows (windows)
        port = 8080
        host = "localhost"

    print(f"Started Running: http://{host}:{port}")
    if not debug:
        serve(app, host=host, port=port)
    else:
        app.run(host=host, port=port)
