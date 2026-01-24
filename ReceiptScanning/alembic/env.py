from logging.config import fileConfig
import os
import sys
from pathlib import Path

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context
from dotenv import load_dotenv

# ensure project root on path so models can be imported when running Alembic
sys.path.append(str(Path(__file__).resolve().parents[1]))

from models.base import Base  # noqa: E402
# Import all models so Alembic sees the full metadata
from models import accounts  # noqa: F401,E402
from models import categories  # noqa: F401,E402
from models import categorization_rules  # noqa: F401,E402
from models import email_reports  # noqa: F401,E402
from models import import_jobs  # noqa: F401,E402
from models import merchants  # noqa: F401,E402
from models import password_reset_tokens  # noqa: F401,E402
from models import products  # noqa: F401,E402
from models import receiptitems  # noqa: F401,E402
from models import receipts  # noqa: F401,E402
from models import transactions  # noqa: F401,E402
from models import user_merchant_preferences  # noqa: F401,E402
from models import user_settings  # noqa: F401,E402
from models import users  # noqa: F401,E402

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

load_dotenv()


def get_url() -> str:
    """Build sync DB URL for Alembic (avoid async driver to prevent MissingGreenlet)."""
    user = os.getenv("DATABASE_USER", "")
    pwd = os.getenv("DATABASE_PASSWORD", "")
    host = os.getenv("DATABASE_HOST", "localhost")
    port = os.getenv("DATABASE_PORT", "3306")
    db = os.getenv("DATABASE_DB", "")
    return f"mysql+pymysql://{user}:{pwd}@{host}:{port}/{db}"

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    config.set_main_option("sqlalchemy.url", get_url())

    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
