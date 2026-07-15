from pydantic import BaseModel, EmailStr

class StudentCreate(BaseModel):
    name: str
    age: int
    department: str
    email: EmailStr

class UserResponse(BaseModel):
    id: int
    username: str
    role: str

    class Config:
        from_attributes = True

class StudentResponse(BaseModel):
    id: int
    name: str
    age: int
    department: str
    email: EmailStr

    user: UserResponse

    class Config:
        from_attributes = True

class StudentListResponse(BaseModel):
    success: bool
    message: str
    data: list[StudentResponse]


class StudentSingleResponse(BaseModel):
    success: bool
    message: str
    data: StudentResponse

class StudentCreateResponse(BaseModel):
    success: bool
    message: str
    data: StudentResponse

class StudentUpdateResponse(BaseModel):
    success: bool
    message: str
    data: StudentResponse

class StudentTrashResponse(BaseModel):
    success: bool
    message: str
    data: list[StudentResponse]

class StudentCountResponse(BaseModel):
    total_students: int


class DepartmentStatsResponse(BaseModel):
    department: str
    total_students: int

class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class MessageResponse(BaseModel):
    success: bool
    message: str
