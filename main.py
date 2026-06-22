from fastapi import FastAPI
from models import Base

from database import engine
from routers import students, users

app = FastAPI()

Base.metadata.create_all(bind=engine)

print("Tables Created Successfully")

app.include_router(students.router)
app.include_router(users.router)

@app.get("/")
def home():
    return {
        "message": "Student Management API Running Successfully"
    }