from fastapi import FastAPI

from routes.student_routes import router as student_router

app = FastAPI(
    title="Student CRUD API",
    description="A simple REST API built with FastAPI to manage university student records using local in-memory storage.",
    version="1.0.0",
)

app.include_router(student_router)


@app.get("/")
def root():
    return {"message": "FastAPI Student CRUD API is running"}
