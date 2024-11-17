import pytest

from reporting.conf import setup_env_variables

@pytest.fixture(scope="session")
def setup_once():
    setup_env_variables()
