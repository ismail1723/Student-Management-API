from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import asc, func
from logger_config import logger

from auth import get_current_user
from database import get_db
from models import Student, User
from schemas import (
    StudentCreate,
    StudentResponse,
    StudentListResponse,
    StudentSingleResponse,
    StudentCreateResponse,
    StudentUpdateResponse,
    StudentTrashResponse,
    StudentCountResponse,
    DepartmentStatsResponse,
    MessageResponse
)

router = APIRouter()

# =========================
# GET ALL STUDENTS
# =========================

@router.get(
    "/students",
    response_model=StudentListResponse
)
def get_students(
    skip: int = 0,
    limit: int = 5,
    department: str = None,
    sort_by: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    query = db.query(Student).filter(
    Student.user_id == current_user.id,
    Student.is_deleted == False
    )

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

    logger.info(
    f"{current_user.username} viewed student list"
    )

    return {
    "success": True,
    "message": "Students fetched successfully",
    "data": students
    }

# =========================
# CREATE STUDENT
# =========================

@router.post(
    "/students",
    response_model=StudentCreateResponse
)
def create_student(
    student: StudentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    db_student = Student(
    name=student.name,
    age=student.age,
    department=student.department,
    email=student.email,
    user_id=current_user.id
    )

    db.add(db_student)
    db.commit()
    db.refresh(db_student)

    logger.info(
    f"Student '{db_student.name}' created by {current_user.username}"
    )

    return {
    "success": True,
    "message": "Student Created Successfully",
    "data": db_student
}

# =========================
# STUDENT COUNT
# =========================

@router.get(
    "/students/count",
    response_model=StudentCountResponse
)

def student_count(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    total_students = db.query(Student).filter(
    Student.user_id == current_user.id,
    Student.is_deleted == False
    ).count()

    logger.info(
        f"{current_user.username} checked total student count"
    )

    return {
        "total_students": total_students
    }

# =========================
# DEPARTMENT STATS
# =========================

@router.get(
    "/students/stats/department",
    response_model=list[DepartmentStatsResponse]
)

def department_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    stats = (
        db.query(
            Student.department,
            func.count(Student.id).label("total_students")
        )
        .filter(
            Student.user_id == current_user.id,
            Student.is_deleted == False
        )
        .group_by(Student.department)
        .all()
    )

    logger.info(
        f"{current_user.username} viewed department statistics"
    )

    result = []

    for department, total_students in stats:
        result.append({
            "department": department,
            "total_students": total_students
        })

    return result

# =========================
# TRASH STUDENTS
# =========================

@router.get(
    "/students/trash",
    response_model=StudentTrashResponse
)

def get_deleted_students(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    students = db.query(Student).filter(
        Student.user_id == current_user.id,
        Student.is_deleted == True
    ).all()

    logger.info(
    f"{current_user.username} viewed trash"
    )

    return {
        "success": True,
        "message": "Deleted students fetched successfully",
        "data": students
    }

# =========================
# SEARCH STUDENT
# =========================

@router.get(
    "/search",
    response_model=StudentSingleResponse
)
def search_student(
    name: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    student = db.query(Student).filter(
    Student.name.ilike(f"%{name}%"),
    Student.user_id == current_user.id,
    Student.is_deleted == False
    ).first()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    logger.info(
    f"Student '{student.name}' searched by {current_user.username}"
    )

    return {
    "success": True,
    "message": "Student found",
    "data": student
    }

# =========================
# GET SINGLE STUDENT
# =========================
@router.get(
    "/students/{student_id}",
    response_model=StudentSingleResponse
)

def get_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    student = db.query(Student).filter(
    Student.id == student_id,
    Student.user_id == current_user.id,
    Student.is_deleted == False
    ).first()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    logger.info(
    f"Student '{student.name}' viewed by {current_user.username}"
    )

    return {
    "success": True,
    "message": "Students fetched successfully",
    "data": student
    }

# =========================
# UPDATE STUDENT
# =========================
@router.put(
    "/students/{student_id}",
    response_model=StudentUpdateResponse
)
def update_student(
    student_id: int,
    student: StudentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_student = db.query(Student).filter(
    Student.id == student_id,
    Student.user_id == current_user.id,
    Student.is_deleted == False
    ).first()

    if db_student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    db_student.name = student.name
    db_student.age = student.age
    db_student.department = student.department
    db_student.email = student.email

    db.commit()
    db.refresh(db_student)

    logger.info(
    f"Student '{db_student.name}' updated by {current_user.username}"
)

    return {
    "success": True,
    "message": "Student Updated Successfully",
    "data": db_student
    }

# =========================
# MOVE TO TRASH
# =========================
@router.delete(
    "/students/{student_id}",
    response_model=MessageResponse
)
def delete_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    student = db.query(Student).filter(
    Student.id == student_id,
    Student.user_id == current_user.id,
    Student.is_deleted == False
    ).first()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    logger.info(
    f"Student '{student.name}' deleted by {current_user.username}"
    )

    student.is_deleted = True

    db.commit()

    return {
    "success": True,
    "message": "Student moved to trash successfully"
    }

# =========================
# RESTORE STUDENT
# =========================
@router.put(
    "/students/{student_id}/restore",
    response_model=MessageResponse
)
def restore_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    student = db.query(Student).filter(
        Student.id == student_id,
        Student.user_id == current_user.id,
        Student.is_deleted == True
    ).first()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    student.is_deleted = False

    db.commit()

    logger.info(
        f"Student '{student.name}' restored by {current_user.username}"
    )

    return {
        "success": True,
        "message": "Student restored successfully"
    }

# =========================
# PERMANENT DELETE
# =========================
@router.delete(
    "/students/{student_id}/permanent",
    response_model=MessageResponse
)
def permanent_delete_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    student = db.query(Student).filter(
        Student.id == student_id,
        Student.user_id == current_user.id,
        Student.is_deleted == True
    ).first()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    db.delete(student)
    db.commit()

    logger.info(
        f"Student '{student.name}' permanently deleted by {current_user.username}"
    )

    return {
        "success": True,
        "message": "Student permanently deleted"
    }