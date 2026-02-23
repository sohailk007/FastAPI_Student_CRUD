from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

from database import SessionLocal, engine
import models, schemas

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Student Management API",
    description="A simple CRUD API for managing students",
    version="1.0.0"
)

# Dependency: get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ─────────────────────────────────────────────
# CREATE
# ─────────────────────────────────────────────
@app.post("/students", response_model=schemas.StudentResponse, status_code=201, tags=["Students"])
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    """Create a new student."""
    # Check for duplicate email
    existing = db.query(models.Student).filter(models.Student.email == student.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="A student with this email already exists.")

    db_student = models.Student(**student.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


# ─────────────────────────────────────────────
# READ ALL
# ─────────────────────────────────────────────
@app.get("/students", response_model=list[schemas.StudentResponse], tags=["Students"])
def get_all_students(db: Session = Depends(get_db)):
    """Retrieve all students."""
    return db.query(models.Student).all()


# ─────────────────────────────────────────────
# READ ONE
# ─────────────────────────────────────────────
@app.get("/students/{id}", response_model=schemas.StudentResponse, tags=["Students"])
def get_student(id: int, db: Session = Depends(get_db)):
    """Retrieve a student by ID."""
    student = db.query(models.Student).filter(models.Student.id == id).first()
    if not student:
        raise HTTPException(status_code=404, detail=f"Student with ID {id} not found.")
    return student


# ─────────────────────────────────────────────
# UPDATE
# ─────────────────────────────────────────────
@app.put("/students/{id}", response_model=schemas.StudentResponse, tags=["Students"])
def update_student(id: int, updated: schemas.StudentCreate, db: Session = Depends(get_db)):
    """Update an existing student by ID."""
    student = db.query(models.Student).filter(models.Student.id == id).first()
    if not student:
        raise HTTPException(status_code=404, detail=f"Student with ID {id} not found.")

    # Check email conflict with another student
    conflict = (
        db.query(models.Student)
        .filter(models.Student.email == updated.email, models.Student.id != id)
        .first()
    )
    if conflict:
        raise HTTPException(status_code=400, detail="Another student already uses this email.")

    student.name = updated.name
    student.email = updated.email
    student.age = updated.age
    db.commit()
    db.refresh(student)
    return student


# ─────────────────────────────────────────────
# DELETE
# ─────────────────────────────────────────────
@app.delete("/students/{id}", tags=["Students"])
def delete_student(id: int, db: Session = Depends(get_db)):
    """Delete a student by ID."""
    student = db.query(models.Student).filter(models.Student.id == id).first()
    if not student:
        raise HTTPException(status_code=404, detail=f"Student with ID {id} not found.")

    db.delete(student)
    db.commit()
    return {"message": f"Student with ID {id} deleted successfully."}