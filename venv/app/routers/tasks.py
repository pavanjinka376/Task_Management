from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.future import select
from app.models import Task
from app.schemas import TaskCreate
from app.database import get_db
from app.dependencies import get_current_user

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/")
async def create_task(task: TaskCreate, db=Depends(get_db), user=Depends(get_current_user)):
    new_task = Task(**task.dict(), owner_id=user.id)
    db.add(new_task)
    await db.commit()
    return {"message": "Task created"}

@router.get("/")
async def list_tasks(db=Depends(get_db), user=Depends(get_current_user)):
    result = await db.execute(select(Task).where(Task.owner_id == user.id))
    return result.scalars().all()

@router.get("/{task_id}")
async def get_task(task_id: str, db=Depends(get_db), user=Depends(get_current_user)):
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(status_code=404)
    if task.owner_id != user.id:
        raise HTTPException(status_code=403)

    return task

@router.delete("/{task_id}")
async def delete_task(task_id: str, db=Depends(get_db), user=Depends(get_current_user)):
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(status_code=404)
    if task.owner_id != user.id:
        raise HTTPException(status_code=403)

    await db.delete(task)
    await db.commit()
    return {"message": "Task deleted"}
@router.put("/{task_id}")
async def update_task(
    task_id: str,
    task_data: TaskCreate,
    db=Depends(get_db),
    user=Depends(get_current_user),
):
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(status_code=404)
    if task.owner_id != user.id:
        raise HTTPException(status_code=403)

    for key, value in task_data.dict().items():
        setattr(task, key, value)

    await db.commit()
    await db.refresh(task)
    return task
