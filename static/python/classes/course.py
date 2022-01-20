# todo: add types
class Course:
    def __init__(self, **kwargs):
        self._id = kwargs.get("_id")
        self.owner = kwargs.get('owner')
        self.name = kwargs.get('name')
        self.teacher = kwargs.get('teacher')
        self.files = kwargs.get('files', [])
        self.grades = kwargs.get('grades', 0)
        self.textbooks = kwargs.get('textbooks', [])
        self.extensions = kwargs.get('extensions', [])

    def to_dict(self):
        return {
            "owner": self.owner,
            "name": self.name,
            "teacher": self.teacher,
            "files": self.files,
            "grades": self.grades,
            "textbooks": self.textbooks,
            "extensions": self.extensions
        }
