from mongoengine import *

from .Snowflake import Snowflake


class Grades(Snowflake):
    course = ReferenceField("Course", required=True)
    student = ReferenceField("User", required=True)
    terms = DictField(ReferenceField("TermGrade"))  # Trimester 1, Trimester 2, etc.

    letter = StringField(required=False)
    percent = FloatField(required=False)

    average = FloatField(required=False)
    median = FloatField(required=False)
    mode = FloatField(required=False)
    range = FloatField(required=False)
    grade_frequency = DictField(required=False)

    def clean(self):
        points = [a.grade for a in self.course.assignments]
        total = [a.points for a in self.course.assignments]
        self.percent = sum(points) / sum(total)
        self.letter = getLetterGrade(self.percent)

        self.average = float(get_average(points))
        self.median = float(get_median(points))
        self.mode = float(get_mode(points))
        self.range = float(get_range(points))
        self.grade_frequency = get_grade_frequency(points)


def getLetterGrade(percent: float):
    percent *= 100
    if percent >= 90:
        return "A"
    elif percent >= 80:
        return "B"
    elif percent >= 70:
        return "C"
    elif percent >= 60:
        return "D"
    else:
        return "F"


def get_average(points):
    return sum(points) / len(points)


def get_median(points):
    points.sort()
    if len(points) % 2 == 0:
        return (points[int(len(points) / 2)] + points[int(len(points) / 2) - 1]) / 2
    return points[int(len(points) / 2)]


def get_mode(points):
    return max(set(points), key=points.count)


def get_range(points):
    return max(points) - min(points)


def get_grade_frequency(points):
    return {str(grade): points.count(grade) for grade in points}
