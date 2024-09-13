import pytest

from api import API


@pytest.fixture
def app():
    return API()
