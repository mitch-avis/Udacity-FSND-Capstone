import json
import pytest

from capstone_app import create_app


@pytest.fixture()
def test_client():
    test_app = create_app()
    test_app.config.update({"TESTING": True})
    with test_app.test_client() as test_client:
        yield test_client


def test_index_page(test_client):
    response = test_client.get(f"/")
    data = json.loads(response.data)
    actual = data["greeting"]

    expected = "Hello"

    assert response.status_code == 200
    assert actual == expected
