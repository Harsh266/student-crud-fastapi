from fastapi import APIRouter, HTTPException, Path, Query, Response, status

from controllers import student_controller
from controllers.student_controller import DuplicateEmailError, StudentNotFoundError
from models.student_model import (
    ErrorResponse,
    StudentCreate,
    StudentListResponse,
    StudentResponse,
    StudentUpdate,
)

router = APIRouter(prefix="/students", tags=["Students"])

StudentId = Path(..., gt=0, description="Unique ID of the student", examples=[1])

NOT_FOUND = {
    status.HTTP_404_NOT_FOUND: {"model": ErrorResponse, "description": "Student not found"}
}
DUPLICATE_EMAIL = {
    status.HTTP_400_BAD_REQUEST: {
        "model": ErrorResponse,
        "description": "Email already used by another student",
    }
}


@router.post(
    "",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a student",
    description="Create a new student record. The ID is generated automatically.",
    response_description="The created student",
    responses=DUPLICATE_EMAIL,
)
def create_student(student: StudentCreate):
    try:
        return student_controller.create_student(student)
    except DuplicateEmailError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get(
    "",
    response_model=StudentListResponse,
    status_code=status.HTTP_200_OK,
    summary="Get all students",
    description=(
        "Return all students. Optional filters: `name` and `course` "
        "(case-insensitive partial match) and `semester` (exact match). "
        "Results are paginated with `page` and `limit`."
    ),
    response_description="A paginated list of students",
)
def get_all_students(
    name: str | None = Query(None, description="Search by name (partial, case-insensitive)", examples=["Rahul"]),
    course: str | None = Query(None, description="Filter by course (partial, case-insensitive)", examples=["BCA"]),
    semester: int | None = Query(None, gt=0, description="Filter by exact semester", examples=[5]),
    page: int = Query(1, ge=1, description="Page number (starts at 1)"),
    limit: int = Query(10, gt=0, le=100, description="Students per page (1-100)"),
):
    filtered = student_controller.get_all_students(name=name, course=course, semester=semester)
    return student_controller.paginate_students(filtered, page=page, limit=limit)


@router.get(
    "/{id}",
    response_model=StudentResponse,
    status_code=status.HTTP_200_OK,
    summary="Get a student by ID",
    description="Return a single student by their unique ID.",
    response_description="The requested student",
    responses=NOT_FOUND,
)
def get_student(id: int = StudentId):
    try:
        return student_controller.get_student_by_id(id)
    except StudentNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put(
    "/{id}",
    response_model=StudentResponse,
    status_code=status.HTTP_200_OK,
    summary="Update a student",
    description="Replace all fields of an existing student. The student ID is preserved.",
    response_description="The updated student",
    responses={**NOT_FOUND, **DUPLICATE_EMAIL},
)
def update_student(student: StudentUpdate, id: int = StudentId):
    try:
        return student_controller.update_student(id, student)
    except StudentNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except DuplicateEmailError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a student",
    description="Delete a student by ID. Returns an empty body on success.",
    response_description="Student deleted (no content)",
    responses=NOT_FOUND,
)
def delete_student(id: int = StudentId):
    try:
        student_controller.delete_student(id)
    except StudentNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return Response(status_code=status.HTTP_204_NO_CONTENT)
