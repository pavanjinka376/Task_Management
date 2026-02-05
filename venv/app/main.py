from fastapi import FastAPI
from sqlalchemy import select
from app.database import engine, Base, AsyncSessionLocal
from app.models import Role
from app.routers import auth, users, tasks

app = FastAPI(title="FastAPI Task Management")

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(tasks.router)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Role))
        roles = result.scalars().all()

        if not roles:
            session.add_all([
                Role(id="admin-role-id", name="ADMIN"),
                Role(id="user-role-id", name="USER")
            ])
            await session.commit()
