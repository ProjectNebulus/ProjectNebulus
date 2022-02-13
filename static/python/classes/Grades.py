from dataclasses import dataclass

@dataclass
class Grades:
    course_id: int
    student_id: int
    _id: int

    def get_average(self):
        return sum(self.grades) / len(self.grades)

    def get_median(self):
        self.grades.sort()
        if len(self.grades) % 2 == 0:
            return (self.grades[int(len(self.grades) / 2)] + self.grades[int(len(self.grades) / 2) - 1]) / 2
        else:
            return self.grades[int(len(self.grades) / 2)]

    def get_mode(self):
        mode = []
        for grade in self.grades:
            if self.grades.count(grade) > len(self.grades) / 2:
                mode.append(grade)
        return mode

    def get_range(self):
        self.grades.sort()
        return self.grades[-1] - self.grades[0]

    def get_grade_frequency(self):
        return [self.grades.count(grade) for grade in self.grades]