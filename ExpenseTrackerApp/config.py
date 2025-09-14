import os
from sqlalchemy.pool import StaticPool
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"

    # Read-only mode prevents disk writes (avatar uploads, etc.)
    READ_ONLY = os.environ.get("READ_ONLY", "1") == "1"

    # Database
    _ENV_DB_URL = os.environ.get("DATABASE_URL")
    if _ENV_DB_URL:
        SQLALCHEMY_DATABASE_URI = _ENV_DB_URL
    else:
        SQLALCHEMY_DATABASE_URI = (
            "sqlite:///:memory:" if READ_ONLY else "sqlite:///expense_tracker.db"
        )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Engine options for in-memory SQLite
    if SQLALCHEMY_DATABASE_URI.endswith(":memory:"):
        SQLALCHEMY_ENGINE_OPTIONS = {
            "poolclass": StaticPool,
            "connect_args": {"check_same_thread": False},
        }

    # Uploads
    UPLOAD_FOLDER = os.path.join(
        os.path.dirname(__file__), "app", "static", "uploads"
    )
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024  # 2MB