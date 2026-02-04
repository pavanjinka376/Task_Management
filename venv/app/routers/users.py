from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.future import select
from app.models import User
from app.database import get_db
from app.dependencies import get_current_user
from app.schemas import UserUpdate

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/")
async def list_users(db=Depends(get_db), current_user=Depends(get_current_user)):
    result = await db.execute(select(User))
    return result.scalars().all()

@router.get("/{user_id}")
async def get_user(user_id: str, db=Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404)
    return user

@router.delete("/{user_id}")
async def delete_user(user_id: str, db=Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404)

    await db.delete(user)
    await db.commit()
    return {"message": "User deleted"}


@router.put("/{user_id}")
async def update_user(
    user_id: str,
    user_data: UserUpdate,
    db=Depends(get_db),
    current_user=Depends(get_current_user),
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404)

    for key, value in user_data.dict(exclude_unset=True).items():
        setattr(user, key, value)

    await db.commit()
    await db.refresh(user)
    return user
