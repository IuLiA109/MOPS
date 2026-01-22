import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
from controller.auth_controller import router as auth_router
from controller.scan_controller import router as scan_router
from controller.transaction_controller import router as transaction_router
from controller.category_controller import router as category_router
from controller.account_controller import router as account_router
from controller.dashboard_controller import router as dashboard_router
from models.base import Base
from db.session import engine, get_db
from helpers.categorization import create_default_categories, create_default_rules


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # create (if not exists) default categories and rules
    async for db in get_db():
        await create_default_categories(db)
        await create_default_rules(db)
        break

    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)
app.include_router(auth_router)
app.include_router(scan_router)
app.include_router(account_router)
app.include_router(transaction_router)
app.include_router(category_router)
app.include_router(dashboard_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)