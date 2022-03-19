from flask import redirect
from . import course
from ....utils.logged_in import logged_in


@course.route('/')
@logged_in
def courses_home(course_id):
    return redirect("/courses/course/" + str(course_id) + "/documents")
