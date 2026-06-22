from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import asc

from auth import get_current_user
from database import get_db
from models import Student
from schemas import StudentCreate, StudentResponse

router = APIRouter()

@router.get(
    "/students",
    response_model=list[StudentResponse]
)
def get_students(
    skip: int = 0,
    limit: int = 5,
    department: str = None,
    sort_by: str = None,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):

    query = db.query(Student)

    if department:
        query = query.filter(
            Student.department == department
        )

    if sort_by == "name":
        query = query.order_by(
            asc(Student.name)
        )

    elif sort_by == "age":
        query = query.order_by(
            asc(Student.age)
        )

    students = query\
        .offset(skip)\
        .limit(limit)\
        .all()

    return students

@router.get(
    "/students/{student_id}",
    response_model=StudentResponse
)
def get_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):

    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student

@router.get(
    "/search",
    response_model=StudentResponse
)
def search_student(
    name: str,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):

    student = db.query(Student).filter(
        Student.name.ilike(f"%{name}%")
    ).first()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student

@router.put("/students/{student_id}")
def update_student(
    student_id: int,
    student: StudentCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    db_student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if db_student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    db_student.name = student.name
    db_student.age = student.age
    db_student.department = student.department

    db.commit()

    return {
        "message": "Student Updated Successfully"
    }

@router.delete("/students/{student_id}")
def delete_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):

    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    db.delete(student)
    db.commit()

    return {
        "message": "Student Deleted Successfully"
    }