from pydantic import BaseModel, EmailStr, Field


class StudentCreate(BaseModel):
    name:  str      = Field(..., min_length=1, max_length=100, examples=["Alice Johnson"])
    email: EmailStr = Field(..., examples=["alice@example.com"])
    age:   int      = Field(..., ge=1, le=120, examples=[20])


class StudentResponse(StudentCreate):
    id: int

    model_config = {"from_attributes": True}