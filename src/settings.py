import os

from sqlalchemy.ext.asyncio import create_async_engine

# Paths
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# FastAPI configuration
APP_HOST = os.environ.get("APP_HOST", "0.0.0.0")
APP_PORT = int(os.environ.get("APP_PORT", "8000"))

# JWT configuration
# change secret before using in production
ACCESS_TOKEN_EXPIRE_MINUTES = 10
TOKEN_URL = "/token"
JWT_SECRET = os.environ.get("JWT_SECRET", "3dbe0c6d-7e09-4bb0-917a-3c36f38eeed0")
ALGORITHM = "HS256"

# Database connection
# use DB settings from your server
DB_NAME = os.environ.get("POSTGRES_DB", "postgres")
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = os.environ.get("DB_PORT", "5432")
DB_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "8e48d41c-7e6d-4503-b152-a5896224c553")
DB_USER = os.environ.get("POSTGRES_USER", "postgres")
DB_ENGINE = os.environ.get("DB_ENGINE", "postgresql+asyncpg")

ENGINE = create_async_engine(f"{DB_ENGINE}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
                             echo=True,
                             )

# Celery
CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")
