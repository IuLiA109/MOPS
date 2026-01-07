import asyncio
import pytest

from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from main import app
from models.base import Base
from db.session import get_db

DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(
	DATABASE_URL,
	connect_args={"check_same_thread": False},
	future=True,
)

@pytest.fixture(scope="session", autouse=True)
def create_test_db():
	async def init_models():
		async with engine.begin() as conn:
			await conn.run_sync(Base.metadata.drop_all)
			await conn.run_sync(Base.metadata.create_all)

	asyncio.run(init_models())
	yield

@pytest.fixture
async def db_session() -> AsyncSession:
	async with engine.connect() as conn:
		trans = await conn.begin()

		SessionLocal = async_sessionmaker(
			bind=conn,
			autoflush=False,
			autocommit=False,
			expire_on_commit=False,
			class_=AsyncSession,
		)

		session = SessionLocal()
		try:
			yield session
		finally:
			await session.close()
			await trans.rollback()

@pytest.fixture(autouse=True)
def override_get_db(db_session: AsyncSession):
	async def _get_test_db():
		yield db_session

	app.dependency_overrides[get_db] = _get_test_db
	yield
	app.dependency_overrides.clear()

@pytest.fixture
async def async_client():
	transport = ASGITransport(app=app)
	async with AsyncClient(transport=transport, base_url="http://test") as client:
		yield client
