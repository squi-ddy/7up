import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    db_host: str
    db_port: str
    db_pass: str
    db_user: str
    db_name: str
    bot_token: str


loaded_settings = Settings(
    db_host=os.environ.get("DB_HOST", "localhost"),
    db_port=os.environ.get("DB_PORT", "5432"),
    db_pass=os.environ.get("DB_PASS", ""),
    db_user=os.environ.get("DB_USER", "postgres"),
    db_name=os.environ.get("DB_NAME", "7up"),
    bot_token=os.environ.get("BOT_TOKEN", ""),
)
