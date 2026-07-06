from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)
    department = Column(String)
    email = Column(String, unique=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    user = relationship(
        "User",
        back_populates="students"
    )


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String, default="user")

    students = relationship(
        "Student",
        back_populates="user"
    )