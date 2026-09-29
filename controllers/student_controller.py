from models.student_model import Student, StudentCreate, StudentUpdate

# In-memory storage: student ID -> Student. No database is used.
students: dict[int, Student] = {}
_next_id = 1


class StudentNotFoundError(Exception):
    """Raised when no student exists with the requested ID."""

    def __init__(self, student_id: int):
        self.student_id = student_id
        super().__init__(f"Student with ID {student_id} not found")


def create_student(data: StudentCreate) -> Student:
    global _next_id
    student = Student(id=_next_id, **data.model_dump())
    students[student.id] = student
    _next_id += 1
    return student


def get_all_students() -> list[Student]:
    return list(students.values())


def get_student_by_id(student_id: int) -> Student:
    student = students.get(student_id)
    if student is None:
        raise StudentNotFoundError(student_id)
    return student


def update_student(student_id: int, data: StudentUpdate) -> Student:
    get_student_by_id(student_id)
    updated = Student(id=student_id, **data.model_dump())
    students[student_id] = updated
    return updated


def delete_student(student_id: int) -> None:
    get_student_by_id(student_id)
    del students[student_id]
