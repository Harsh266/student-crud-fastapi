from fastapi import APIRouter, HTTPException, Path, Query, Response, status

from controllers import student_controller
from controllers.student_controller import DuplicateEmailError, StudentNotFoundError
from models.student_model import (
    StudentCreate,
    StudentListResponse,
    StudentResponse,
    StudentUpdate,
)

router = APIRouter(prefix="/students", tags=["Students"])

StudentId = Path(..., gt=0)


@router.post("", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(student: StudentCreate):
    try:
        return student_controller.create_student(student)
    except DuplicateEmailError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("", response_model=StudentListResponse, status_code=status.HTTP_200_OK)
def get_all_students(
    name: str | None = Query(None),
    course: str | None = Query(None),
    semester: int | None = Query(None, gt=0),
    page: int = Query(1, ge=1),
    limit: int = Query(10, gt=0, le=100),
):
    filtered = student_controller.get_all_students(name=name, course=course, semester=semester)
    return student_controller.paginate_students(filtered, page=page, limit=limit)


@router.get("/{id}", response_model=StudentResponse, status_code=status.HTTP_200_OK)
def get_student(id: int = StudentId):
    try:
        return student_controller.get_student_by_id(id)
    except StudentNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/{id}", response_model=StudentResponse, status_code=status.HTTP_200_OK)
def update_student(student: StudentUpdate, id: int = StudentId):
    try:
        return student_controller.update_student(id, student)
    except StudentNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except DuplicateEmailError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(id: int = StudentId):
    try:
        student_controller.delete_student(id)
    except StudentNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return Response(status_code=status.HTTP_204_NO_CONTENT)
