from fastapi.testclient import TestClient


def test_get_activities_returns_all_activities(client: TestClient):
    # Arrange
    expected_keys = {"description", "schedule", "max_participants", "participants"}

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert data
    assert "Chess Club" in data
    assert all(expected_keys.issubset(activity.keys()) for activity in data.values())


def test_signup_new_participant_adds_email_to_activity(client: TestClient):
    # Arrange
    activity_name = "Chess Club"
    email = "teststudent@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert email in response.json()["message"]

    activities = client.get("/activities").json()
    assert email in activities[activity_name]["participants"]


def test_signup_duplicate_participant_returns_400(client: TestClient):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_delete_participant_removes_email_from_activity(client: TestClient):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert email in response.json()["message"]

    activities = client.get("/activities").json()
    assert email not in activities[activity_name]["participants"]


def test_delete_nonexistent_participant_returns_404(client: TestClient):
    # Arrange
    activity_name = "Chess Club"
    email = "missingstudent@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert "Participant not found" in response.json()["detail"]
