# 🎓 Student Management API

A FastAPI CRUD application with SQLite database and Swagger UI.

---

## 📁 Project Structure

```
student_api/
├── main.py          # FastAPI app & all route handlers
├── database.py      # SQLAlchemy engine & session setup
├── models.py        # ORM model (Student table)
├── schemas.py       # Pydantic request/response schemas
├── requirements.txt # Python dependencies
└── README.md
```

---

## ⚙️ Setup & Run

**Prerequisite:** Python 3.12+

### 1. Create a virtual environment (recommended)
```bash
python -m venv venv
source venv/bin/activate        # Linux / Mac
venv\Scripts\activate           # Windows
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Start the server
```bash
uvicorn main:app --reload
```

The API will be available at: **http://127.0.0.1:8000**

---

## 📖 Swagger UI

Open your browser and go to:

```
http://127.0.0.1:8000/docs
```

All endpoints are fully documented and testable from Swagger UI.

---

## 🔌 API Endpoints

| Method | Endpoint            | Description          |
|--------|---------------------|----------------------|
| POST   | `/students`         | Create a new student |
| GET    | `/students`         | Get all students     |
| GET    | `/students/{id}`    | Get student by ID    |
| PUT    | `/students/{id}`    | Update student       |
| DELETE | `/students/{id}`    | Delete student       |

---

## 📦 Request / Response Examples

### ➕ Create Student — `POST /students`

**Request Body:**
```json
{
  "name": "Alice Johnson",
  "email": "alice@example.com",
  "age": 20
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "name": "Alice Johnson",
  "email": "alice@example.com",
  "age": 20
}
```

---

### 📋 Get All Students — `GET /students`

**Response (200 OK):**
```json
[
  { "id": 1, "name": "Alice Johnson", "email": "alice@example.com", "age": 20 },
  { "id": 2, "name": "Bob Smith",     "email": "bob@example.com",   "age": 22 }
]
```

---

### 🔍 Get Student by ID — `GET /students/1`

**Response (200 OK):**
```json
{ "id": 1, "name": "Alice Johnson", "email": "alice@example.com", "age": 20 }
```

**Error (404 Not Found):**
```json
{ "detail": "Student with ID 1 not found." }
```

---

### ✏️ Update Student — `PUT /students/1`

**Request Body:**
```json
{
  "name": "Alice Williams",
  "email": "alice.w@example.com",
  "age": 21
}
```

**Response (200 OK):**
```json
{ "id": 1, "name": "Alice Williams", "email": "alice.w@example.com", "age": 21 }
```

---

### 🗑️ Delete Student — `DELETE /students/1`

**Response (200 OK):**
```json
{ "message": "Student with ID 1 deleted successfully." }
```

---

## 🗄️ Database

- **Type:** SQLite  
- **File:** `students.db` (auto-created in project folder on first run)  
- **Table:** `students` with columns: `id`, `name`, `email`, `age`

---

## ✅ Completion Checklist

- [x] FastAPI app runs without errors  
- [x] POST `/students` — creates a student  
- [x] GET `/students` — lists all students  
- [x] GET `/students/{id}` — fetch by ID with 404 error if not found  
- [x] PUT `/students/{id}` — updates student with 404 error if not found  
- [x] DELETE `/students/{id}` — deletes student with success message  
- [x] Swagger UI available at `/docs`  
- [x] SQLite database table created automatically  
- [x] Duplicate email validation  
- [x] Proper error messages for all failure cases