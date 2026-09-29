from fastapi import APIRouter, status

from controllers import student_controller
from models.student_model import Student, StudentCreate

router = APIRouter(prefix="/students", tags=["Students"])


@router.post("", response_model=Student, status_code=status.HTTP_201_CREATED)
def create_student(student: StudentCreate):
    return student_controller.create_student(student)
