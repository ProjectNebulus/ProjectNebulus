class Course:
    def __init__(self, owner, name, teacher, files, grades, textbooks, extensions):
        self.owner = owner
        self.name = name
        self.teacher = teacher
        self.files = files
        self.grades = grades
        self.textbooks = textbooks
        self.extensions = extensions
    def to_dictionary(self):
        the_dictionary = {
        "owner" : self.owner,
        "name": self.name,
        "teacher" : self.teacher,
        "files" : self.files,
        "grades" : self.grades,
        "textbooks" :self.textvooks,
        "extensions": self.extensions
        }
        return the_dictionary