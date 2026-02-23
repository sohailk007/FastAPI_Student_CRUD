from pydantic import BaseModel, EmailStr, Field 

class StudentCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, example="Saim Khan")
    email: EmailStr = Field(..., example="saim@gmail.com")
    age: int = Field(..., ge=0, le=150, example=25)
    
class StudentResponse(StudentCreate):
    id: int
    
    class Config:
        orm_mode = True 