class MyInterface:
    def items_from_dict(self, dictionary: dict) -> list[float]:
        result = []
        for grade in dictionary.values():
            result += grade
        return result


class Student(MyInterface):
    def __init__(self, name: str, surname: str, gender: str):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def __str__(self):
        if len(self.grades):
            return (f"Имя: {self.name}\nФамилия: {self.surname}\nСредняя оценка за домашние задания: "
                    f"{self.average_grade()}\n"
                    f"Курсы в процессе изучения: {', '.join(self.courses_in_progress)}\n"
                    f"Завершенные курсы: {', '.join(self.finished_courses)}\n")
        else:
            return (f"Имя: {self.name}\nФамилия: {self.surname}\nСредняя оценка за домашние задания: 0.0\n"
                    f"Курсы в процессе изучения: {', '.join(self.courses_in_progress)}\n"
                    f"Завершенные курсы: {', '.join(self.finished_courses)}\n")

    def __eq__(self, other):
        return self.average_grade() == other.average_grade()

    def __ne__(self, other):
        return self.average_grade() != other.average_grade()

    def __lt__(self, other):
        return self.average_grade() < other.average_grade()

    def __gt__(self, other):
        return self.average_grade() > other.average_grade()

    def __le__(self, other):
        return self.average_grade() <= other.average_grade()

    def __ge__(self, other):
        return self.average_grade() >= other.average_grade()

    def lecturer_rate(self, rate: float, course: str, lecturer):
        if isinstance(lecturer, Lecturer):
            lecturer.courses_rates[course] += [rate]
        else:
            return "Ошибка"

    def average_grade(self) -> float:
        return sum(self.items_from_dict(self.grades)) / len(self.grades)


class Mentor(MyInterface):
    def __init__(self, name: str, surname: str):
        self.name = name
        self.surname = surname
        self.courses_attached = []

    def update_courses(self, course: str):
        if course in self.courses_attached:
            return
        self.courses_attached.append(course)


class Lecturer(Mentor):
    def __init__(self, name: str, surname: str):
        super().__init__(name, surname)
        self.courses_rates = dict()

    def __str__(self):
        if len(self.courses_rates):
            return (f"Имя: {self.name}\nФамилия: {self.surname}\nСредняя оценка за лекции: "
                    f"{self.average_grade()}\n")
        else:
            return f"Имя: {self.name}\nФамилия: {self.surname}\nСредняя оценка за лекции: 0.0\n"

    def __eq__(self, other):
        return self.average_grade() == other.average_grade()

    def __ne__(self, other):
        return self.average_grade() != other.average_grade()

    def __lt__(self, other):
        return self.average_grade() < other.average_grade()

    def __gt__(self, other):
        return self.average_grade() > other.average_grade()

    def __le__(self, other):
        return self.average_grade() <= other.average_grade()

    def __ge__(self, other):
        return self.average_grade() >= other.average_grade()

    def average_grade(self) -> float:
        return sum(self.items_from_dict(self.courses_rates)) / len(self.courses_rates.values())

    def update_courses(self, course: str):
        if course in self.courses_rates.keys():
            return
        self.courses_attached.append(course)
        self.courses_rates[course] = []


class Reviewer(Mentor):
    def __str__(self):
        return f"Имя: {self.name}\nФамилия: {self.surname}\n"

    def rate_hw(self, student: Student, course: str, grade: float):
        if course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'


def average_grade_for_hw_by_course(students: list[Student], course: str) -> float:
    grades = 0
    grades_num = 0
    for st in students:
        grades += sum(st.grades[course])
        grades_num += len(st.grades[course])
    return round(grades / grades_num, 2)

def average_grade_for_lection_by_course(lecturer: list[Lecturer], course: str) -> float:
    grades = 0
    grades_num = 0
    for lec in lecturer:
        grades += sum(lec.courses_rates[course])
        grades_num += len(lec.courses_rates[course])
    return round(grades / grades_num, 2)

if __name__ == "__main__":
    reviewer1 = Reviewer("R1", "R1")
    lecturer1 = Lecturer("L1", "L1")
    student1 = Student("S1", "S1", "Male")
    reviewer2 = Reviewer("R2", "R2")
    lecturer2 = Lecturer("L2", "L2")
    student2 = Student("S2", "S2", "Female")

    reviewer1.update_courses("Py")
    reviewer2.update_courses("Py")
    reviewer1.update_courses("Git")
    lecturer1.update_courses("Py")
    lecturer2.update_courses("Py")
    lecturer1.update_courses("Git")
    student1.courses_in_progress += ["Py"]
    student2.courses_in_progress += ["Py"]
    student1.courses_in_progress += ["Git"]
    reviewer1.rate_hw(student1, "Py", 5)
    reviewer1.rate_hw(student1, "Git", 4)
    reviewer2.rate_hw(student2, "Py", 2)
    reviewer2.rate_hw(student1, "Py", 2)
    student1.lecturer_rate(10, "Py", lecturer1)
    student1.lecturer_rate(9, "Git", lecturer1)
    student2.lecturer_rate(1, "Py", lecturer2)
    student2.lecturer_rate(3, "Py", lecturer2)
    print(reviewer1, reviewer2, lecturer1, lecturer2, student1, student2, sep="\n", end="")
    print(student1 > student2)
    print(student1 == student2)
    print(lecturer1 < lecturer2)
    print(lecturer1 >= lecturer2)
    print(average_grade_for_hw_by_course([student1, student2], "Py"))
    print(average_grade_for_lection_by_course([lecturer1, lecturer2], "Py"))
