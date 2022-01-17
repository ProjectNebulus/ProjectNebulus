# todo: add types
class Course:
    def __init__(self, **kwargs):
        self._id = kwargs.get("_id")
        self.owner = kwargs.get('owner')
        self.name = kwargs.get('name')
        self.teacher = kwargs.get('teacher')
        self.files = kwargs.get('files') or []
        self.grades = kwargs.get('grades') or 0
        self.textbooks = kwargs.get('textbooks') or []
        self.extensions = kwargs.get('extensions') or []

    def to_dictionary(self):
        return {
            "owner": self.owner,
            "name": self.name,
            "teacher": self.teacher,
            "files": self.files,
            "grades": self.grades,
            "textbooks": self.textbooks,
            "extensions": self.extensions
        }
