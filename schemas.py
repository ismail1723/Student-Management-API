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

class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str