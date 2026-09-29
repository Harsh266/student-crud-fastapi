from pydantic import BaseModel, EmailStr, Field, field_validator


class StudentBase(BaseModel):
    """Fields shared by every student model."""

    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    course: str = Field(..., min_length=1, max_length=100)
    semester: int = Field(..., gt=0, le=12)

    @field_validator("name", "course")
    @classmethod
    def must_not_be_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("must not be empty or only whitespace")
        return value


class StudentCreate(StudentBase):
    """Request body for creating a student."""


class StudentUpdate(StudentBase):
    """Request body for updating (replacing) a student."""


class Student(StudentBase):
    """A stored student record."""

    id: int


class StudentResponse(BaseModel):
    """A single student as returned by the API."""

    id: int
    name: str
    email: EmailStr
    course: str
    semester: int


class StudentListResponse(BaseModel):
    """A paginated, optionally filtered list of students."""

    page: int
    limit: int
    total: int
    total_pages: int
    students: list[StudentResponse]
