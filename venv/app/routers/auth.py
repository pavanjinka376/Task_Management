from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.future import select
from app.schemas import UserRegister, UserLogin
from app.models import User
from app.database import get_db
from app.auth import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
async def register(user: UserRegister, db=Depends(get_db)):
    result = await db.execute(select(User).where(User.email == user.email))
    if result.scalar():
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        email=user.email,
        hashed_password=hash_password(user.password),
        role_id=user.role_id
    )
    db.add(new_user)
    await db.commit()
    return {"message": "User registered successfully"}

@router.post("/login")
async def login(data: UserLogin, db=Depends(get_db)):
    result = await db.execute(select(User).where(User.email == data.email))
    user = result.scalar_one_or_none()

    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user.id})
    return {"access_token": token, "token_type": "bearer"}
