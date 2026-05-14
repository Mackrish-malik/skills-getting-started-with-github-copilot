"""Tests for GET /activities endpoint using AAA (Arrange-Act-Assert) pattern"""
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_all_activities_returns_complete_list():
    # ARRANGE: No setup needed for read-only operation
    
    # ACT
    response = client.get("/activities")
    
    # ASSERT
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "Gym Class" in data


def test_get_activities_returns_correct_activity_structure():
    # ARRANGE: Expected activity fields
    required_fields = {"description", "schedule", "max_participants", "participants"}
    
    # ACT
    response = client.get("/activities")
    data = response.json()
    
    # ASSERT
    activity = data["Chess Club"]
    assert set(activity.keys()) == required_fields
    assert isinstance(activity["participants"], list)
    assert isinstance(activity["max_participants"], int)


def test_get_activities_includes_participant_data():
    # ARRANGE
    expected_chess_participants = ["michael@mergington.edu", "daniel@mergington.edu"]
    
    # ACT
    response = client.get("/activities")
    data = response.json()
    
    # ASSERT
    assert data["Chess Club"]["participants"] == expected_chess_participants
    assert len(data["Programming Class"]["participants"]) == 2
