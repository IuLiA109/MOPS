import os
import pytest
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()
user = os.getenv("DATABASE_USER")
password = os.getenv("DATABASE_PASSWORD")
host = os.getenv("DATABASE_HOST")
port = os.getenv("DATABASE_PORT")
database = os.getenv("DATABASE_DB")

DATABASE_URL = "mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(
            user, password, host, port, database
        )

engine = db.create_engine(
    DATABASE_URL,
    future=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


def get_db():
    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()