import datetime
from pathlib import Path

from flask import redirect, render_template, request, send_file, session

from app.static.python.mongodb.read import getText
from . import main_blueprint
from .. import babel


@babel.localeselector
def get_locale():
    if session.get("lang") == "es":
        return "es"
    else:
        return "en"


@main_blueprint.route("/screenTime", methods=["GET"])
def screenTime():
    data = int(request.args.get("data"))
    location = request.args.get("location")
    print(
        f"[Screen Time Log | {datetime.date.today()} @ '{location}'] {data / 1000} seconds "
    )
    return str(data)


@main_blueprint.route("/getSchoolEmbed/<school>", methods=["GET"])
def schoolEmbed(school):
    import imgkit

    imgkit.from_file("./app/templates/joinschoolembed.html", f"{school}.jpg")
    return send_file(f"{school}.jpg")


@main_blueprint.route("/school", methods=["GET"])
def school():
    import json

    myjson = json.load(open("app/schools.json"))
    return render_template(
        "school.html",
        page="Select your School",
        user=session.get("username"),
        user_id=session.get("id"),
        email=session.get("email"),
        avatar=session.get("avatar", "/static/images/nebulusCats/v3.gif", ),
        translate=getText,
        schools=myjson,
    )


@main_blueprint.route("/invite/school/<school>", methods=["GET"])
def specificschool(school):
    school = school.upper()
    schools = [
        "BISV",
        "HKR",
        "CBYA",
        "MLR",
        "SDPB",
        "VCS",
        "PNLK",
        "BCP",
        "GUNN",
        "PALY",
        "LNBK",
        "CLGBA",
        "NBLS"
    ]
    if school not in schools:
        return render_template("errors/404.html", translate=getText), 404
    import json

    myjson = json.load(open("app/schools.json"))
    for current in myjson:
        if current["code"] == school:
            return render_template(
                "joinschool.html",
                school=current,
                page="Nebulus. Education. Redefined.",
                user=session.get("username"),
                user_id=session.get("id"),
                email=session.get("email"),
                avatar=session.get("avatar", "/static/images/nebulusCats/v3.gif", ),
                translate=getText,
                homepage=True,
                embedoverride=True,
            )


@main_blueprint.route("/", methods=["GET"])
def index():
    return render_template(
        "main/index.html",
        page="Nebulus. Education. Redefined.",
        user=session.get("username"),
        user_id=session.get("id"),
        email=session.get("email"),
        avatar=session.get("avatar", "/static/images/nebulusCats/v3.gif", ),
        translate=getText,
        homepage=True,
    )


@main_blueprint.route("/google34d8c04c4b82b69a.html")
def googleVerification():
    # GOOGLE VERIFICATION FILE
    return render_template("utils/google_site_verification.html", translate=getText)


@main_blueprint.route("/arc-sw.js")
def arcstuff():
    return redirect("https://arc.io/arc-sw.js")


@main_blueprint.route("/privacy-policy")
def pp():
    return render_template(
        "privacy.html",
        translate=getText,
        user=session.get("username"),
        user_id=session.get("id"),
        email=session.get("email"),
        avatar=session.get("avatar", "/static/images/nebulusCats/v3.gif"),
        homepage=True,
    )


@main_blueprint.route("/terms-of-service")
def tos():
    return render_template(
        "tos.html",
        translate=getText,
        user=session.get("username"),
        user_id=session.get("id"),
        email=session.get("email"),
        avatar=session.get("avatar", "/static/images/nebulusCats/v3.gif"),
        homepage=True,
    )


@main_blueprint.route("/select-a-region")
def selectregion():
    return render_template(
        "main/select-a-region.html",
        user=session.get("username"),
        user_id=session.get("id"),
        email=session.get("email"),
        avatar=session.get("avatar", "/static/images/nebulusCats/v3.gif"),
        page="Select a Region",
        translate=getText,
        homepage=True,
    )

@main_blueprint.route("/global/<country>")
def globalcountry(country):
    session["global"] = country
    return redirect("/")

@main_blueprint.app_errorhandler(404)
@main_blueprint.app_errorhandler(400)
def page_not_found(e):
    path = request.path
    # print(path)
    if len(path.strip("/")) == 2:
        return redirect(f"/global{path}")
    # note that we set the 404 status explicitly
    return (
        render_template(
            "errors/404.html",
            page="Not Found",
            user=session.get("username"),
            user_id=session.get("id"),
            email=session.get("email"),
            avatar=session.get("avatar", "/static/images/nebulusCats/v3.gif"),
            translate=getText,
        ),
        404,
    )


@main_blueprint.app_errorhandler(500)
def internal_error(e):
    # note that we set the 500 status explicitly
    return (
        render_template(
            "errors/500.html",
            page="Nebulus is Down",
            user=session.get("username"),
            user_id=session.get("id"),
            email=session.get("email"),
            avatar=session.get("avatar", "/static/images/nebulusCats/v3.gif"),
            translate=getText,
        ),
        500,
    )


@main_blueprint.route("/sw.js")
def sw():
    path = Path(__file__)
    print(path.parent.parent.parent)
    return send_file(str(path.parent.parent.parent) + "/static/js/sw.js")


@main_blueprint.route("/sitemap.xml")
def sitemap():
    path = Path(__file__)
    print(path.parent.parent.parent)
    return send_file(str(path.parent.parent.parent) + "/static/sitemap.xml")


@main_blueprint.route("/study/session")
def studyplanner():
    return render_template(
        "learning/tools/study-planner.html",
        user=session.get("username"),
        user_id=session.get("id"),
        email=session.get("email"),
        avatar=session.get("avatar", "/static/images/nebulusCats/v3.gif"),
        page="Study Planner",
        translate=getText,
    )


@main_blueprint.route("/lunch")
def lunchplanner():
    return render_template(
        "learning/tools/lunch.html",
        user=session.get("username"),
        user_id=session.get("id"),
        email=session.get("email"),
        avatar=session.get("avatar", "/static/images/nebulusCats/v3.gif"),
        page="Lunch Planner",
        translate=getText,
    )


@main_blueprint.route("/vacation")
def vacationmode():
    return render_template(
        "learning/tools/vacation.html",
        user=session.get("username"),
        user_id=session.get("id"),
        email=session.get("email"),
        avatar=session.get("avatar", "/static/images/nebulusCats/v3.gif"),
        page="Vacation Mode",
        translate=getText,
    )


@main_blueprint.route("/extra-curricular")
def extracurricular():
    return render_template(
        "learning/tools/extra-curricular.html",
        user=session.get("username"),
        user_id=session.get("id"),
        email=session.get("email"),
        avatar=session.get("avatar", "/static/images/nebulusCats/v3.gif"),
        page="Extracurricular Mode",
        translate=getText,
    )


@main_blueprint.route("/study/analytics")
def analysis():
    return render_template(
        "learning/tools/analysis.html",
        user=session.get("username"),
        user_id=session.get("id"),
        email=session.get("email"),
        avatar=session.get("avatar", "/static/images/nebulusCats/v3.gif"),
        page="Study Planner",
        translate=getText,
    )


@main_blueprint.route("/blog")
def blog():
    return render_template(
        "main/blog.html",
        user=session.get("username"),
        user_id=session.get("id"),
        email=session.get("email"),
        avatar=session.get("avatar", "/static/images/nebulusCats/v3.gif"),
        page="Blog",
        translate=getText,
    )


@main_blueprint.route("/upgrade")
def upgrade():
    return render_template(
        "upgrade.html",
        user=session.get("username"),
        user_id=session.get("id"),
        email=session.get("email"),
        avatar=session.get("avatar", "/static/images/nebulusCats/v3.gif"),
        page="Upgrade",
        translate=getText,
    )


@main_blueprint.route("/support")
def support():
    return render_template(
        "main/support.html",
        user=session.get("username"),
        user_id=session.get("id"),
        email=session.get("email"),
        avatar=session.get("avatar", "/static/images/nebulusCats/v3.gif"),
        page="Support",
        translate=getText,
    )
