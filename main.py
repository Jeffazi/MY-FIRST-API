from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel
from fastapi import Response

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

class TaskUpdate(BaseModel):
    title: str
    done: bool

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

@app.get("/tasks/{id}",
    summary="Get task by ID",
    description="Returns the details of a specific task identified by its ID.")
def get_task(id: int):
    for task in tasks:
        if task["id"] == id:
            return task

    return JSONResponse(
        status_code=404,
        content={"error": f"Task 99 not found"}
     )


@app.post("/tasks", status_code=201,
    summary="Create a task",
    description="Creates a new task, assigns it a unique ID, marks it as not completed, and returns the created task.")
def create_task(task: TaskCreate):
    if task.title.strip() == "":
        return JSONResponse(
            status_code=400,
            content={
                "error": "Title cannot be empty"
            }
        )
    
    
    largest_id = max((task["id"] for task in tasks), default=0)
    next_id = largest_id + 1



    new_task = {
        "id": next_id,
        "title": task.title,
        "done": False
    }

    tasks.append(new_task)

    return new_task


@app.put("/tasks/{id}",
    summary="Update a task",
    description="Updates the task identified by its ID and returns the updated task if successful.")
def update_task(id: int, task: TaskUpdate):
    
    if task.title.strip() == "":
        return JSONResponse(
            status_code=400,
            content={
                "error": "Title cannot be empty"
            }
        )
    

    for current_task in tasks:
        if current_task["id"] == id:

            current_task["title"] = task.title
            current_task["done"] = task.done

            return current_task

    return JSONResponse(
        status_code=404,
        content={
            "error": f"Task {id} not found"
        }
    )


@app.delete("/tasks/{id}",
    summary="Delete a task",
    description="Deletes the task identified by its ID and returns a 204 No Content response if successful.")
def delete_task(id: int):

    for current_task in tasks:

        if current_task["id"] == id:

            tasks.remove(current_task)

            return Response(status_code=204)

    return JSONResponse(
        status_code=404,
        content={
            "error": f"Task {id} not found"
        }
    )
    