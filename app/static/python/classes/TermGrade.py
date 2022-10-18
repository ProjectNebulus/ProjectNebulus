from mongoengine import *
from . import GradingCategory


class TermGrade(EmbeddedDocument):
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

    title = StringField(required=True)
    start_date = DateTimeField(required=True)
    end_date = DateTimeField(required=True)
    grading_categories = ListField(EmbeddedDocumentField(GradingCategory))
    grade = FloatField(required=False)

    def clean(self):
        self.grade = sum([grading_category.grade*grading_category.weight for grading_category in self.grading_categories])



