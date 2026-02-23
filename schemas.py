from pydantic import BaseModel, EmailStr, Field


class StudentCreate(BaseModel):
    name:  str      = Field(..., min_length=1, max_length=100, example="Alice Johnson")
    email: EmailStr = Field(..., example="alice@example.com")
    age:   int      = Field(..., ge=1, le=120, example=20)


class StudentResponse(StudentCreate):
    id: int

    model_config = {"from_attributes": True}  # Pydantic v2 (replaces orm_mode)