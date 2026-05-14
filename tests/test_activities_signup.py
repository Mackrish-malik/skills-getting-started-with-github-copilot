"""Tests for POST /activities/{activity_name}/signup endpoint using AAA pattern"""
from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)

def test_signup_student_adds_email_to_participants():
    # ARRANGE
    activity_name = "Tennis Club"
    email = "newstudent@mergington.edu"
    initial_count = len(activities[activity_name]["participants"])
    
    # ACT
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # ASSERT
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"
    assert email in activities[activity_name]["participants"]
    assert len(activities[activity_name]["participants"]) == initial_count + 1


def test_signup_for_nonexistent_activity_returns_404():
    # ARRANGE
    activity_name = "Nonexistent Club"
    email = "student@mergington.edu"
    
    # ACT
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # ASSERT
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_duplicate_student_adds_twice():
    # ARRANGE: Test documents current behavior (bug: allows duplicate signup)
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already registered
    initial_count = len(activities[activity_name]["participants"])
    
    # ACT
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # ASSERT: Currently allows duplicate (bug)
    assert response.status_code == 200
    assert email in activities[activity_name]["participants"]
    # This assertion documents the bug - participant appears twice
    assert activities[activity_name]["participants"].count(email) == 2
    assert len(activities[activity_name]["participants"]) == initial_count + 1


def test_signup_multiple_students_success():
    # ARRANGE
    activity_name = "Art Studio"
    students = [
        "student1@mergington.edu",
        "student2@mergington.edu",
        "student3@mergington.edu"
    ]
    
    # ACT
    for email in students:
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        # ASSERT: Each signup succeeds
        assert response.status_code == 200
    
    # ASSERT: All students are registered
    for email in students:
        assert email in activities[activity_name]["participants"]
