from unittest.mock import patch
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Scientific Search MVP API"


def test_ask_gemini_endpoint():
    with patch("src.main.get_gemini_response", return_value="Это тестовый ответ"):
        response = client.post(
            "/api/ask", json={"query": "Что такое машинное обучение?"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "question" in data
        assert "answer" in data
        assert data["answer"] == "Это тестовый ответ"


def test_empty_query():
    response = client.post("/api/ask", json={"query": ""})
    assert response.status_code == 400
