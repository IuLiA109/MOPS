import pytest
from main import app
from sqlalchemy.orm import sessionmaker
import sqlalchemy as db
from models.base import Base
from httpx import AsyncClient, ASGITransport
from db.session import get_db


DATABASE_URL = "sqlite+pysqlite:///:memory:"

engine = db.create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    future=True,
)

TestingSessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)

@pytest.fixture(scope="session", autouse=True)
def create_test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(autouse=True)
def override_get_db(db_session):
    def _get_test_db():
        yield db_session

    app.dependency_overrides[get_db] = _get_test_db
    yield
    app.dependency_overrides.clear()


@pytest.fixture
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
