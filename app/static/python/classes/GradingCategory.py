from mongoengine import *


class GradingCategory(EmbeddedDocument):
    weight = FloatField(required=True)
    course = ReferenceField('Course', required=True)
    title = StringField(required=True)
    subcategories = ListField(ReferenceField('GradingCategory'), required=False)
    grade = FloatField(required=False)

    def clean(self):
        if self.subcategories:
            self.grade = sum([subcategory.weight*subcategory.grade for subcategory in self.subcategories])
        else:
            points = sum([assignment.points for assignment in self.course.assignments])
            grades = sum([assignment.grade for assignment in self.course.assignments])
            self.grade = grades/points
