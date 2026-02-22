from pathlib import Path
import os
from dotenv import load_dotenv

# Project root (safe way)
BASE_DIR = Path(__file__).resolve().parent

# Load .env from project root
env_path = BASE_DIR / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)

def get_database_url() -> str:
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise RuntimeError("DATABASE_URL is not set.")
    return db_url