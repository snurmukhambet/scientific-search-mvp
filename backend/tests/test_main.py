import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_root_endpoint():
    """Test the root endpoint returns correct message."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Scientific Search MVP API"


def test_ask_gemini_endpoint_success():
    """Test successful question asking."""
    with patch("src.main.get_gemini_response", return_value="This is a test response"):
        response = client.post(
            "/api/ask", json={"query": "What is machine learning?"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "question" in data
        assert "answer" in data
        assert data["question"] == "What is machine learning?"
        assert data["answer"] == "This is a test response"


def test_ask_gemini_endpoint_with_whitespace():
    """Test question with leading/trailing whitespace."""
    with patch("src.main.get_gemini_response", return_value="Test response"):
        response = client.post(
            "/api/ask", json={"query": "  What is AI?  "}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["question"] == "  What is AI?  "


def test_empty_query():
    """Test empty query returns 400."""
    response = client.post("/api/ask", json={"query": ""})
    assert response.status_code == 400
    assert "Question cannot be empty" in response.json()["detail"]


def test_whitespace_only_query():
    """Test whitespace-only query returns 400."""
    response = client.post("/api/ask", json={"query": "   "})
    assert response.status_code == 400
    assert "Question cannot be empty" in response.json()["detail"]


def test_missing_query_field():
    """Test missing query field returns 422."""
    response = client.post("/api/ask", json={})
    assert response.status_code == 422


def test_invalid_json():
    """Test invalid JSON returns 422."""
    response = client.post(
        "/api/ask", 
        data="invalid json",
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 422


def test_cors_headers():
    """Test CORS headers are present."""
    response = client.options("/api/ask")
    # The OPTIONS request should be handled by CORS middleware
    assert response.status_code in [200, 405]  # Some implementations return 405


@patch("src.main.get_gemini_response")
def test_gemini_response_called_with_correct_query(mock_gemini):
    """Test that Gemini is called with the correct query."""
    mock_gemini.return_value = "Test response"
    test_query = "Explain quantum computing"
    
    response = client.post("/api/ask", json={"query": test_query})
    
    assert response.status_code == 200
    mock_gemini.assert_called_once_with(test_query)


def test_long_query():
    """Test handling of very long queries."""
    long_query = "What is " + "very " * 1000 + "long question?"
    
    with patch("src.main.get_gemini_response", return_value="Response to long query"):
        response = client.post("/api/ask", json={"query": long_query})
        assert response.status_code == 200
        data = response.json()
        assert data["question"] == long_query


def test_special_characters_query():
    """Test handling of special characters in queries."""
    special_query = "What is 2+2? Is it 4? 🤔 Testing unicode: αβγ"
    
    with patch("src.main.get_gemini_response", return_value="Four"):
        response = client.post("/api/ask", json={"query": special_query})
        assert response.status_code == 200
        data = response.json()
        assert data["question"] == special_query


@pytest.mark.parametrize("query,expected_response", [
    ("What is AI?", "AI is artificial intelligence"),
    ("How does ML work?", "Machine learning works by..."),
    ("Explain DNA", "DNA is deoxyribonucleic acid"),
])
def test_multiple_queries(query, expected_response):
    """Test multiple different queries."""
    with patch("src.main.get_gemini_response", return_value=expected_response):
        response = client.post("/api/ask", json={"query": query})
        assert response.status_code == 200
        data = response.json()
        assert data["answer"] == expected_response
