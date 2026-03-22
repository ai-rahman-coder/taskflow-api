from app.schemas.task_schema import TaskCreate, TaskReplace, TaskResponse, TaskUpdate


# Temporary in-memory storage for tasks
tasks_db = []
task_id_counter = 1

def create_task(task: TaskCreate) -> TaskResponse:
    global task_id_counter

    new_task = TaskResponse(
        id = task_id_counter,
        title = task.title,
        description = task.description
    )

    tasks_db.append(new_task)
    task_id_counter += 1

    return new_task


def get_tasks() -> list[TaskResponse]:
    return tasks_db

def get_task_by_id(task_id: int) -> TaskResponse | None:
    for task in tasks_db:
        if task.id == task_id:
            return task
    return None


def delete_task(task_id: int) -> bool:
    for i, task in enumerate(tasks_db):
        if task.id == task_id:
            del tasks_db[i]
            return True
    return False


def replace_task(task_id: int, updated_task: TaskReplace) -> TaskResponse | None:
    for task in tasks_db:
        if task.id == task_id:
            task.title = updated_task.title
            task.description = updated_task.description
            return task
    return None


def update_task(task_id: int, updated_task: TaskUpdate) -> TaskResponse | None:
    for task in tasks_db:
        if task.id == task_id:
            if updated_task.title is not None:
                task.title = updated_task.title
            if updated_task.description is not None:
                task.description = updated_task.description
            return task
    return None

