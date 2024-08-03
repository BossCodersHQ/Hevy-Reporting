import os

def get_hevy_api_root_url():
    return os.getenv("HEVY_API_ROOT_URL", "https://api.hevyapp.com")