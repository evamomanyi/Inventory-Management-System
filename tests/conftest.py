import pytest
from app import app
from models import inventory


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def reset_inventory():
    original = [item.copy() for item in inventory]
    yield
    inventory.clear()
    inventory.extend(original)
