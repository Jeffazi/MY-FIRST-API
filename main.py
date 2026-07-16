from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.responses import JSONResponse

app = FastAPI()

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
    