from mongoengine import *


class GradingCategory(EmbeddedDocument):
    CALC_PERCENTAGE = 1
    CALC_TOTAL_PTS = 2

    course = ReferenceField("Course")
    weight = FloatField(default=1, description="Weight (in decimal) of this category.")
    title = StringField(default=None, null=True, required=True)
    subcategories = ListField(EmbeddedDocumentField("GradingCategory"), required=False, default=[])
    grade = FloatField(required=False)
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

                self.grade = grades / max_grade

            else:
                grades = []
                for assignment in self.course.assignments:
                    if assignment.grading_category is self:
                        grades.append(assignment.points / assignment.grade)

                if len(grades) > 0:
                    self.grade = sum(grades) / len(grades)
                else:
                    self.grade = 1

    def __str__(self):
        return f'GradingCategory(title="{self.title}", weight={self.weight})'
