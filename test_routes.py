from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_create_book():
    response = client.post("/book/", json={"title": "Test Book", "author_id": 1})
    assert response.status_code == 200
    assert "id" in response.json()


def test_get_all_books():
    response = client.get("/books/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
