from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional

from app.services.task_service import create_task, get_tasks, get_task_by_id, delete_task, replace_task, update_task
from app.schemas.task_schema import TaskCreate, TaskResponse, TaskUpdate, TaskReplace

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("", response_model=TaskResponse)
def create_task_api(task: TaskCreate):
    return create_task(task)

@router.get("", response_model=List[TaskResponse])
def get_tasks_api(title: Optional[str] = Query(None)):
    tasks = get_tasks()
    if title:
        tasks = [task for task in tasks if title.lower() in task.title.lower()]
    return tasks

@router.get("/{task_id}", response_model=TaskResponse)
def get_task_by_id_api(task_id: int):
    task = get_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return task

@router.delete("/{task_id}")
def delete_task_api(task_id: int):
    success = delete_task(task_id)

    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return {"message": "Task deleted successfully"}

@router.put("/{task_id}", response_model=TaskResponse)
def replace_task_api(task_id: int, task: TaskReplace):
    updated = replace_task(task_id, task)
    if not updated:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return updated

@router.patch("/{task_id}", response_model=TaskResponse)
def update_task_api(task_id: int, task: TaskUpdate):
    updated = update_task(task_id, task)
    if not updated:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return updated