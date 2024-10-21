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
                    f"{sum(self.items_from_dict(self.grades))/len(self.grades)}\n"
                    f"Курсы в процессе изучения: {', '.join(self.courses_in_progress)}\n"
                    f"Завершенные курсы: {', '.join(self.finished_courses)}\n")
        else:
            return (f"Имя: {self.name}\nФамилия: {self.surname}\nСредняя оценка за домашние задания: 0.0\n"
                    f"Курсы в процессе изучения: {', '.join(self.courses_in_progress)}\n"
                    f"Завершенные курсы: {', '.join(self.finished_courses)}\n")

    def lecturer_rate(self, rate: float, course: str, lecturer):
        if isinstance(lecturer, Lecturer):
            lecturer.courses_rates[course] += [rate]
        else:
            return "Ошибка"


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
                    f"{sum(self.items_from_dict(self.courses_rates)) / len(self.courses_rates.values())}\n")
        else:
            return f"Имя: {self.name}\nФамилия: {self.surname}\nСредняя оценка за лекции: 0.0\n"

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
    student1.lecturer_rate(10, "Py", lecturer1)
    student1.lecturer_rate(9, "Git", lecturer1)
    student2.lecturer_rate(1, "Py", lecturer2)
    print(reviewer1, reviewer2, lecturer1, lecturer2, student1, student2, sep="\n", end="")
