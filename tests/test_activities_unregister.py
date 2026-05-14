"""Tests for DELETE /activities/{activity_name}/unregister endpoint using AAA pattern"""
from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)

def test_unregister_student_removes_from_participants():
    # ARRANGE
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already registered
    initial_count = len(activities[activity_name]["participants"])
    
    # ACT
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    
    # ASSERT
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"
    assert email not in activities[activity_name]["participants"]
    assert len(activities[activity_name]["participants"]) == initial_count - 1


def test_unregister_nonexistent_student_returns_400():
    # ARRANGE
    activity_name = "Chess Club"
    nonexistent_email = "notregistered@mergington.edu"
    initial_count = len(activities[activity_name]["participants"])
    
    # ACT
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": nonexistent_email}
    )
    
    # ASSERT
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is not registered for this activity"
    # Verify no participants were removed
    assert len(activities[activity_name]["participants"]) == initial_count


def test_unregister_from_nonexistent_activity_returns_404():
    # ARRANGE
    activity_name = "Nonexistent Club"
    email = "student@mergington.edu"
    
    # ACT
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    
    # ASSERT
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_all_participants_success():
    # ARRANGE
    activity_name = "Tennis Club"
    participants = activities[activity_name]["participants"].copy()
    
    # ACT & ASSERT: Unregister each participant
    for email in participants:
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        assert response.status_code == 200
    
    # ASSERT: Activity is now empty
    assert len(activities[activity_name]["participants"]) == 0
