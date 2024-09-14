import pytest

from api import API


@pytest.fixture
def app():
    return API()


@pytest.fixture
def client(app):
    return app.test_session()
