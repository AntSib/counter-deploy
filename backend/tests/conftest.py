import os
import pytest
from app import app, r, COUNTER_KEY


@pytest.fixture(autouse=True)
def reset_counter():
    """
    Перед каждым тестом:
    - сбрасываем счётчик
    """
    r.set(COUNTER_KEY, 0)
    yield
    r.set(COUNTER_KEY, 0)


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client
