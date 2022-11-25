from mongoengine import *


class GradingCategory(EmbeddedDocument):
    CALC_PERCENTAGE = 1
    CALC_TOTAL_PTS = 2

    course = ReferenceField("Course")
    weight = FloatField(default=None, description="Weight (in decimal) of this category.")
    title = StringField(default=None)
    subcategories = ListField(EmbeddedDocumentField("GradingCategory"), default=None)
    grade = FloatField(required=False)
    show_in_upcoming = BooleanField(default=False)
    calculation_type = IntField(default=CALC_PERCENTAGE)
    imported_id = StringField(required=True)

    def clean(self):
        if self.subcategories:
            self.grade = sum(
                [
                    subcategory.weight * subcategory.grade
                    for subcategory in self.subcategories
                ]
            )

        else:
            if self.calculation_type == self.CALC_TOTAL_PTS:
                max_grade = sum(
                    [assignment.points for assignment in self.course.assignments if assignment.grading_category is self]
                )
                grades = sum(
                    [assignment.grade for assignment in self.course.assignments if assignment.grading_category is self]
                )

                if max_grade > 0:
                    self.grade = grades / max_grade
                else:
                    self.grade = 1

            else:
                grades = []
                for assignment in self.course.assignments:
                    if assignment.grading_category is self and assignment.points and assignment.grade is not None:
                        grades.append(assignment.grade / assignment.points)

                if len(grades) > 0:
                    self.grade = sum(grades) / len(grades)
                else:
                    self.grade = 1

    def __str__(self):
        return f'GradingCategory(title="{self.title}", weight={self.weight})'

    def __hash__(self):
        return hash(" ".join(map(str, self._fields_ordered)))
