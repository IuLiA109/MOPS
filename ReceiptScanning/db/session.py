import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = "mysql+aiomysql://{0}:{1}@{2}:{3}/{4}".format(
    os.getenv("DATABASE_USER"),
    os.getenv("DATABASE_PASSWORD"),
    os.getenv("DATABASE_HOST"),
    os.getenv("DATABASE_PORT"),
    os.getenv("DATABASE_DB")
)

engine = create_async_engine(
    DATABASE_URL,
    future=True,
    pool_pre_ping=True
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()