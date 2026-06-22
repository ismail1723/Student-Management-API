from pydantic import BaseModel

class StudentCreate(BaseModel):
    name: str
    age: int
    department: str

class StudentResponse(BaseModel):
    id: int
    name: str
    age: int
    department: str

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str