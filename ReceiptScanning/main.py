import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
from controller.auth_controller import router as auth_router
from controller.scan_controller import router as scan_router
from models.base import Base
from db.session import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)
app.include_router(auth_router)
app.include_router(scan_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)