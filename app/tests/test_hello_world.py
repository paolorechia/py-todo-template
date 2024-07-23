from litestar.status_codes import HTTP_200_OK
from litestar.testing import TestClient

from src.main import litestar_app


def test_health_check():
    with TestClient(app=litestar_app) as client:
        response = client.get("/")
        assert response.status_code == HTTP_200_OK
        items = response.json()
        assert items[0]["name"] == "test-item"
        assert items[0]["status"] == "todo"
