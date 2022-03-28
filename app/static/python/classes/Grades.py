from typing import Dict, List

from mongoengine import *

from .Snowflake import Snowflake


class Grades(Snowflake):
    """
    Class to store the grades of a student in one course.
    :params:
        - student_id: The student's id.
        - course_id: The course's id.
        - grades: The grades of the student in the course. Is expected to be a dictionary in the format:
            {assignment_id: [grade, weight]} OR {grades_id} to Nest
        Default: {}
    :autogenerated attributes:
        - grades_list: A list of the student's grades with the weight taken into account.
        - average: The average of the student's grades.
        - median: The median of the student's grades.
        - mode: The mode of the student's grades.
        - range: The range of the student's grades.
        - grade_frequency: A dictionary with the frequency of each grade.
    """

    course = ReferenceField("Course", required=True)
    student = ReferenceField("User", required=True)
    grades = DictField(required=True)
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
