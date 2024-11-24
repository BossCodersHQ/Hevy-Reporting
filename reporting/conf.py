import os
from dotenv import load_dotenv
import logging
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


def get_root_package_path():
    """Return the root package path"""
    return os.path.dirname(os.path.realpath(__file__))

def get_dot_env_path():
    """Return the path to the .env file"""
    return os.path.join(os.path.dirname(get_root_package_path()), ".env")

def initialise_app():
    """Initialise the application"""
    setup_logging()
    get_settings()


def setup_logging():
    """Setup logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s:Line:%(lineno)d - %(levelname)s - %(message)s",
        datefmt="%d-%b-%y %H:%M:%S",
    )

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=get_dot_env_path())

    hevy_api_root_url: str = "https://api.hevyapp.com"
    hevy_api_key: str


@lru_cache(maxsize=1)
def get_settings() -> Settings:
   return Settings()
