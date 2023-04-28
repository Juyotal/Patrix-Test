import pytest
from api.server import app

@pytest.fixture()
def api():
    return app