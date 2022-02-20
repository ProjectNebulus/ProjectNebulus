from mongoengine import *
from typing import Dict, List

from .Snowflake import Snowflake


class Grades(Snowflake):
    """
    Class to store the grades of a student in one course.
    :params:
        - student_id: The student's id.
        - course_id: The course's id.
        - grades: The grades of the student in the course. Is expected to be a dictionary in the format:
            {assignment_id: [grade, weight]}
        Default: {}
    :autogenerated attributes:
        - grades_list: A list of the student's grades with the weight taken into account.
        - average: The average of the student's grades.
        - median: The median of the student's grades.
        - mode: The mode of the student's grades.
        - range: The range of the student's grades.
        - grade_frequency: A dictionary with the frequency of each grade.
    """

    course = ReferenceField('Course', required=True)
    student = ReferenceField('Student', required=True)
    grades = DictField(required=True)
    average = FloatField(required=False)
    median = FloatField(required=False)
    mode = FloatField(required=False)
    range = FloatField(required=False)
    grade_frequency = ListField(FloatField(), required=False)

    def clean(self):
        grades_list = list(self.grades.values())
        self.average = get_average(grades_list)
        self.median = get_median(grades_list)
        self.mode = get_mode(grades_list)
        self.range = get_range(grades_list)
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
    mode = []
    for grade in grades_list:
        if grades_list.count(grade) > len(grades_list) / 2:
            mode.append(grade)
    return mode


def get_range(grades_list):
    grades_list.sort()
    return grades_list[-1] - grades_list[0]


def get_grade_frequency(grades_list):
    return {grade: grades_list.count(grade) for grade in grades_list}
