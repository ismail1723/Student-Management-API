from fastapi import FastAPI
from models import Base
from middleware import log_requests

from database import engine
from routers import students, users
from exception_handler import add_exception_handlers

app = FastAPI()

app.middleware("http")(log_requests)

add_exception_handlers(app)

Base.metadata.create_all(bind=engine)

print("Tables Created Successfully")

app.include_router(students.router)
app.include_router(users.router)

@app.get("/")
def home():
    return {
        "message": "Student Management API Running Successfully"
    }