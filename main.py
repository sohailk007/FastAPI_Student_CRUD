from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from database import SessionLocal, engine
import models, schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Student Management API",
    description="CRUD API for managing students",
    version="1.0.0"
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/students", response_model=schemas.StudentResponse, status_code=201, tags=["Students"])
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    """Create a new student."""
    if db.query(models.Student).filter(models.Student.email == student.email).first():
        raise HTTPException(status_code=400, detail="Email already registered.")
    db_student = models.Student(**student.model_dump())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


@app.get("/students", response_model=List[schemas.StudentResponse], tags=["Students"])
def get_all_students(db: Session = Depends(get_db)):
    """Get all students."""
    return db.query(models.Student).all()


@app.get("/students/{id}", response_model=schemas.StudentResponse, tags=["Students"])
def get_student(id: int, db: Session = Depends(get_db)):
    """Get a student by ID."""
    student = db.query(models.Student).filter(models.Student.id == id).first()
    if not student:
        raise HTTPException(status_code=404, detail=f"Student with ID {id} not found.")
    return student


@app.put("/students/{id}", response_model=schemas.StudentResponse, tags=["Students"])
def update_student(id: int, updated: schemas.StudentCreate, db: Session = Depends(get_db)):
    """Update a student by ID."""
    student = db.query(models.Student).filter(models.Student.id == id).first()
    if not student:
        raise HTTPException(status_code=404, detail=f"Student with ID {id} not found.")
    conflict = db.query(models.Student).filter(
        models.Student.email == updated.email,
        models.Student.id != id
    ).first()
    if conflict:
        raise HTTPException(status_code=400, detail="Email already used by another student.")
    student.name = updated.name
    student.email = updated.email
    student.age = updated.age
    db.commit()
    db.refresh(student)
    return student


@app.delete("/students/{id}", tags=["Students"])
def delete_student(id: int, db: Session = Depends(get_db)):
    """Delete a student by ID."""
    student = db.query(models.Student).filter(models.Student.id == id).first()
    if not student:
        raise HTTPException(status_code=404, detail=f"Student with ID {id} not found.")
    db.delete(student)
    db.commit()
    return {"message": f"Student with ID {id} deleted successfully."}