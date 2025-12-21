from __future__ import annotations

import os
from pathlib import Path


class Settings:
    # Base directory
    BASE_DIR: Path = Path(__file__).resolve().parents[1]
    
    # Database
    DATA_DIR: Path = BASE_DIR / "data"
    DB_PATH: Path = DATA_DIR / "app.db"
    
    # LLM Settings
    LLM_MODEL: str = "llama3.1:8b"
    SKIP_LLM_TESTS: bool = os.getenv("SKIP_LLM_TESTS", "false").lower() == "true"
    
    # Environment fixes
    NO_PROXY: str = "localhost,127.0.0.1"


settings = Settings()

# Apply environment fixes
os.environ["NO_PROXY"] = settings.NO_PROXY
