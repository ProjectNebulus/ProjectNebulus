from mongoengine import *

# noinspection PyUnresolvedReferences
from .GradingCategory import GradingCategory
from .Snowflake import Snowflake
from .TermGrade import TermGrade


class Grades(Snowflake):
    course = ReferenceField("Course", required=True)
    student = ReferenceField("User", required=True)
    terms = ListField(EmbeddedDocumentField(TermGrade), default=[])  # Trimester 1, Trimester 2, etc.

    letter = StringField(required=False)
    grade = FloatField(required=False)

    def clean(self):
        if len(self.terms) == 0:
            self.grade = 100
        else:
            self.grade = sum([term.grade for term in self.terms]) / len(self.terms)
        self.letter = getLetterGrade(self.grade)


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
    return 100 if len(points) == 0 else sum(points) / len(points)


def get_median(points):
    points.sort()
    if len(points) == 0:
        return 100
    if len(points) % 2 == 0:
        return (points[int(len(points) / 2)] + points[int(len(points) / 2) - 1]) / 2
    return points[int(len(points) / 2)]


def get_mode(points):
    return max(set(points), key=points.count) if len(points) > 0 else 100


def get_range(points):
    return 0 if len(points) == 0 else max(points) - min(points)


def get_grade_frequency(points):
    return {str(grade): points.count(grade) for grade in points}
