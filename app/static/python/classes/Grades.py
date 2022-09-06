from mongoengine import *

from .Snowflake import Snowflake


class Grades(Snowflake):
    course = ReferenceField("Course", required=True)
    student = ReferenceField("User", required=True)
    terms = DictField(ReferenceField("TermGrade"))  # Trimester 1, Trimester 2, etc.

    average = FloatField(required=False)
    median = FloatField(required=False)
    mode = FloatField(required=False)
    range = FloatField(required=False)
    grade_frequency = DictField(required=False)

    def clean(self):
        grades_list = list(self.grades.values())
        self.average = float(get_average(grades_list))
        self.median = float(get_median(grades_list))
        self.mode = float(get_mode(grades_list))
        self.range = float(get_range(grades_list))
        self.grade_frequency = get_grade_frequency(grades_list)


def get_average(grades_list):
    return sum(grades_list) / len(grades_list)


def get_median(grades_list):
    grades_list.sort()
    if len(grades_list) % 2 == 0:
        return (
            grades_list[int(len(grades_list) / 2)]
            + grades_list[int(len(grades_list) / 2) - 1]
        ) / 2
    return grades_list[int(len(grades_list) / 2)]


def get_mode(grades_list):
    return max(set(grades_list), key=grades_list.count)


def get_range(grades_list):
    grades_list.sort()
    return grades_list[-1] - grades_list[0]


def get_grade_frequency(grades_list):
    return {str(grade): grades_list.count(grade) for grade in grades_list}
