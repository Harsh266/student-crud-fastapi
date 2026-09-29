from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

STUDENT_EXAMPLE = {
    "name": "Rahul Patel",
    "email": "rahul@example.com",
    "course": "B.Tech Computer Engineering",
    "semester": 5,
}


class StudentBase(BaseModel):
    """Fields shared by every student model."""

    name: str = Field(..., min_length=1, max_length=100, description="Student full name")
    email: EmailStr = Field(..., description="Valid student email address (must be unique)")
    course: str = Field(..., min_length=1, max_length=100, description="Course/program name")
    semester: int = Field(..., gt=0, le=12, description="Current semester (1-12)")

    @field_validator("name", "course")
    @classmethod
    def must_not_be_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("must not be empty or only whitespace")
        return value


class StudentCreate(StudentBase):
    """Request body for creating a student."""

    model_config = ConfigDict(json_schema_extra={"examples": [STUDENT_EXAMPLE]})


class StudentUpdate(StudentBase):
    """Request body for updating (replacing) a student."""

    model_config = ConfigDict(
        json_schema_extra={"examples": [{**STUDENT_EXAMPLE, "semester": 6}]}
    )


class Student(StudentBase):
    """A stored student record."""

    id: int


class StudentResponse(BaseModel):
    """A single student as returned by the API."""

    id: int = Field(..., description="Unique student ID")
    name: str = Field(..., description="Student full name")
    email: EmailStr = Field(..., description="Student email address")
    course: str = Field(..., description="Course/program name")
    semester: int = Field(..., description="Current semester")

    model_config = ConfigDict(json_schema_extra={"examples": [{"id": 1, **STUDENT_EXAMPLE}]})


class StudentListResponse(BaseModel):
    """A paginated, optionally filtered list of students."""

    page: int = Field(..., description="Current page number")
    limit: int = Field(..., description="Maximum students per page")
    total: int = Field(..., description="Total students matching the filters")
    total_pages: int = Field(..., description="Total number of pages")
    students: list[StudentResponse] = Field(..., description="Students on this page")


class ErrorResponse(BaseModel):
    """Error body returned for 400 and 404 responses."""

    detail: str = Field(..., examples=["Student with ID 999 not found"])
