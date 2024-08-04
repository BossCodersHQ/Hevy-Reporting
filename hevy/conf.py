import os
from dotenv import load_dotenv
import logging

def initialise_app():
    """Initialise the application"""
    setup_logging()
    setup_env_variables()


def setup_logging():
    """Setup logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s:Line:%(lineno)d - %(levelname)s - %(message)s",
        datefmt="%d-%b-%y %H:%M:%S",
    )

def setup_env_variables():
    """Setup env variables for the app to run properly"""
    print(get_dot_env_path())
    load_dotenv(dotenv_path=get_dot_env_path())


def get_dot_env_path():
    """Return the path to the .env file"""
    return os.path.join(os.path.dirname(get_root_package_path()), ".env")


def get_root_package_path():
    """Return the root package path"""
    return os.path.dirname(os.path.realpath(__file__))


def get_hevy_api_root_url():
    """Get the root URL for the hevy API"""
    return os.getenv("HEVY_API_ROOT_URL", "https://api.hevyapp.com")


def get_hevy_api_key():
    """Get the Hevy API key"""
    return os.environ["HEVY_API_KEY"]
