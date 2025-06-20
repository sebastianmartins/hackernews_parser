"""
Tests for the HackerNews Parser FastAPI application.
"""

import json
from pathlib import Path
from typing import Any

from fastapi.testclient import TestClient

from hackernews_parser.api import app

client = TestClient(app)


def load_test_data(version: str) -> Any:
    """Load test data for the specified version."""
    data_file = Path(__file__).parent.parent / "data" / f"hackernews_{version}.json"
    with open(data_file) as f:
        return json.load(f)


def test_health_check():
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_root_endpoint():
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "docs" in data
    assert "health" in data


def test_parse_v1_data():
    """Test parsing version 1.0 data."""
    test_data = load_test_data("v1")

    response = client.post("/parse", json=test_data)
    assert response.status_code == 200

    result = response.json()
    assert result["version"] == "1.0"
    assert "stories" in result
    assert len(result["stories"]) == 2

    # Check first story structure
    story = result["stories"][0]
    assert "id" in story
    assert "title" in story
    assert "comments" in story
    # V1 should not have sentiment or relationships
    assert "sentiment" not in story
    assert "relationships" not in story


def test_parse_v2_data():
    """Test parsing version 2.0 data."""
    test_data = load_test_data("v2")

    response = client.post("/parse", json=test_data)
    assert response.status_code == 200

    result = response.json()
    assert result["version"] == "2.0"
    assert "stories" in result
    assert "metrics" in result

    # Check first story structure with v2 features
    story = result["stories"][0]
    assert "sentiment" in story
    assert "relationships" in story

    # Check comment has sentiment
    comment = story["comments"][0]
    assert "sentiment" in comment


def test_missing_version():
    """Test error handling when version field is missing."""
    test_data = {"stories": []}  # Missing version field

    response = client.post("/parse", json=test_data)
    assert response.status_code == 400
    assert "Missing 'version' field" in response.json()["detail"]


def test_unsupported_version():
    """Test error handling for unsupported version."""
    test_data = {"version": "3.0", "stories": []}

    response = client.post("/parse", json=test_data)
    assert response.status_code == 400
    assert "Unsupported version: 3.0" in response.json()["detail"]


def test_invalid_data_structure():
    """Test error handling for invalid data structure."""
    test_data = {"version": "1.0"}  # Missing required fields

    response = client.post("/parse", json=test_data)
    assert response.status_code == 500
    assert "Failed to parse data" in response.json()["detail"]
