from fastapi import APIRouter, HTTPException, Response, status

from controllers import student_controller
from controllers.student_controller import StudentNotFoundError
from models.student_model import Student, StudentCreate, StudentUpdate

router = APIRouter(prefix="/students", tags=["Students"])


@router.post("", response_model=Student, status_code=status.HTTP_201_CREATED)
def create_student(student: StudentCreate):
    return student_controller.create_student(student)


@router.get("", response_model=list[Student], status_code=status.HTTP_200_OK)
def get_all_students():
    return student_controller.get_all_students()


@router.get("/{id}", response_model=Student, status_code=status.HTTP_200_OK)
def get_student(id: int):
    try:
        return student_controller.get_student_by_id(id)
    except StudentNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/{id}", response_model=Student, status_code=status.HTTP_200_OK)
def update_student(id: int, student: StudentUpdate):
    try:
        return student_controller.update_student(id, student)
    except StudentNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(id: int):
    try:
        student_controller.delete_student(id)
    except StudentNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return Response(status_code=status.HTTP_204_NO_CONTENT)
