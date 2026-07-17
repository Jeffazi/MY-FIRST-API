from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel

app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={
            "error": "Title is required"
        }
    )

tasks = [
    ...
]


tasks = [
    {
        "id": 1,
        "title": "Buy milk",
        "done": False
    },
    {
        "id": 2,
        "title": "Study FastAPI",
        "done": False
    },
    {
        "id": 3,
        "title": "Repair laptop",
        "done": True
    }
]


class TaskCreate(BaseModel):
    title: str

@app.get("/")
def home():
    return {
    "name": "Task API",
    "version": "1.0",
    "endpoints": ["/tasks"]
    }

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/tasks")
def get_tasks():
    return tasks

@app.get("/tasks/{id}")
def get_task(id: int):
    for task in tasks:
        if task["id"] == id:
            return task

    return JSONResponse(
        status_code=404,
        content={"error": f"Task 99 not found"}
     )


@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):
    if task.title.strip() == "":
        return JSONResponse(
            status_code=400,
            content={
                "error": "Title cannot be empty"
            }
        )
    
    
    next_id = len(tasks) + 1



    new_task = {
        "id": next_id,
        "title": task.title,
        "done": False
    }

    tasks.append(new_task)

    return new_task
    