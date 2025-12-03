import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_signup_success():
    email = "newstudent@mergington.edu"
    response = client.post("/activities/Chess Club/signup?email=" + email)
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]
    # Clean up
    client.post(f"/activities/Chess Club/unregister?email={email}")


def test_signup_duplicate():
    email = "michael@mergington.edu"
    response = client.post(f"/activities/Chess Club/signup?email={email}")
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_full():
    # Fill up activity
    activity = "Basketball Team"
    max_participants = 15
    for i in range(2, max_participants+1):
        email = f"test{i}@mergington.edu"
        client.post(f"/activities/{activity}/signup?email={email}")
    # Try to sign up one more
    response = client.post(f"/activities/{activity}/signup?email=overflow@mergington.edu")
    assert response.status_code == 400
    assert "Activity is full" in response.json()["detail"]
    # Clean up
    for i in range(2, max_participants+1):
        email = f"test{i}@mergington.edu"
        client.post(f"/activities/{activity}/unregister?email={email}")


def test_signup_missing_activity():
    response = client.post("/activities/Nonexistent/signup?email=someone@mergington.edu")
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_signup_missing_email():
    response = client.post("/activities/Chess Club/signup?email=")
    assert response.status_code == 400
    assert "Email is required" in response.json()["detail"]


def test_unregister_success():
    email = "removeme@mergington.edu"
    client.post(f"/activities/Chess Club/signup?email={email}")
    response = client.post(f"/activities/Chess Club/unregister?email={email}")
    assert response.status_code == 200
    assert "Removed" in response.json()["message"]


def test_unregister_not_registered():
    email = "notregistered@mergington.edu"
    response = client.post(f"/activities/Chess Club/unregister?email={email}")
    assert response.status_code == 200
    assert "was not registered" in response.json()["message"]


def test_unregister_missing_activity():
    response = client.post("/activities/Nonexistent/unregister?email=someone@mergington.edu")
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_unregister_missing_email():
    response = client.post("/activities/Chess Club/unregister?email=")
    assert response.status_code == 400
    assert "Email is required" in response.json()["detail"]
