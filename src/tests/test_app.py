import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    # Check structure
    activity = data[0]
    assert "id" in activity
    assert "name" in activity
    assert "description" in activity
    assert "participants" in activity

def test_signup_success():
    # Use a test email
    email = "test@example.com"
    activity_id = "chess"
    response = client.post(f"/activities/{activity_id}/signup?email={email}")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data

    # Check if added
    response = client.get("/activities")
    activities = response.json()
    chess = next(a for a in activities if a["id"] == "chess")
    assert email in chess["participants"]

def test_signup_already_signed():
    email = "test@example.com"
    activity_id = "chess"
    # Already signed from previous test
    response = client.post(f"/activities/{activity_id}/signup?email={email}")
    assert response.status_code == 400
    data = response.json()
    assert "already signed up" in data["detail"]

def test_signup_invalid_activity():
    email = "test2@example.com"
    activity_id = "invalid"
    response = client.post(f"/activities/{activity_id}/signup?email={email}")
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]

def test_unregister_success():
    email = "test@example.com"
    activity_id = "chess"
    response = client.delete(f"/activities/{activity_id}/unregister?email={email}")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data

    # Check if removed
    response = client.get("/activities")
    activities = response.json()
    chess = next(a for a in activities if a["id"] == "chess")
    assert email not in chess["participants"]

def test_unregister_not_signed():
    email = "notsigned@example.com"
    activity_id = "chess"
    response = client.delete(f"/activities/{activity_id}/unregister?email={email}")
    assert response.status_code == 400
    data = response.json()
    assert "not signed up" in data["detail"]

def test_unregister_invalid_activity():
    email = "test@example.com"
    activity_id = "invalid"
    response = client.delete(f"/activities/{activity_id}/unregister?email={email}")
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]

def test_root_redirect():
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307  # Redirect
    assert response.headers["location"] == "/static/index.html"