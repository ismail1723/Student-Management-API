from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from logger_config import logger

from database import get_db
from models import User
from schemas import (
    UserCreate,
    UserLogin,
    UserResponse,
    StudentResponse
)
from auth import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user,
    get_admin_user
)

router = APIRouter()


@router.post("/register")
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter(
        User.username == user.username
    ).first()

    if existing_user:

        logger.warning(
            f"Registration failed. Username already exists: {user.username}"
        )

        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    hashed_password = hash_password(
        user.password
    )

    new_user = User(
        username=user.username,
        password=hashed_password,
        role="user"
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    logger.info(
        f"New user registered: {new_user.username}"
    )

    return {
        "message": "User registered successfully",
        "user_id": new_user.id
    }


@router.post("/login")
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    db_user = db.query(User).filter(
        User.username == form_data.username
    ).first()

    if not db_user:

        logger.warning(
            f"Failed login attempt for username: {form_data.username}"
        )

        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    if not verify_password(
        form_data.password,
        db_user.password
    ):

        logger.warning(
            f"Wrong password for user: {db_user.username}"
        )

        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    token = create_access_token(
        {"sub": db_user.username}
    )

    logger.info(
        f"User logged in: {db_user.username}"
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@router.get(
    "/me",
    response_model=UserResponse
)
def get_me(
    current_user: User = Depends(get_current_user)
):
    return current_user


@router.get(
    "/my-students",
    response_model=list[StudentResponse]
)
def my_students(
    current_user: User = Depends(get_current_user)
):
    return current_user.students


@router.get("/admin/users")
def get_all_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    users = db.query(User).all()

    logger.info(
        f"Admin {current_user.username} viewed all users"
    )

    return users