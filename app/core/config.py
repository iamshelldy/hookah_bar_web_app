from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_NAME: str

    model_config = SettingsConfigDict(env_file=Path(__file__).parents[2] / ".env")


settings = Settings()


PAGE_METADATA = {
    "title": "Some Lounge",
    "copyright": f"2019-2024 Some Lounge",
    "gm_url": "https://maps.app.goo.gl/4NXw1EFWve7Edbkk9",
    "inst_url": "https://www.instagram.com/",
    "tg_url": "https://t.me/",
}


def get_db_url():
    return f"sqlite+aiosqlite:///{Path(__file__).parents[2]}/{settings.DB_NAME}.db"
