from urllib.parse import quote


def test_get_activities_returns_all(client):
    # Arrange
    activity = "Chess Club"
    expected_description = "Learn strategies and compete in chess tournaments"

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    payload = response.json()
    assert activity in payload
    assert payload[activity]["description"] == expected_description
    assert "participants" in payload[activity]


def test_signup_adds_participant(client):
    # Arrange
    activity = "Chess Club"
    email = "teststudent@mergington.edu"
    url = f"/activities/{quote(activity)}/signup?email={quote(email)}"

    # Act
    response = client.post(url)

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity}"}

    activities = client.get("/activities").json()
    assert email in activities[activity]["participants"]


def test_signup_duplicate_returns_400(client):
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"
    url = f"/activities/{quote(activity)}/signup?email={quote(email)}"

    # Act
    response = client.post(url)

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_delete_participant_removes_participant(client):
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"
    url = f"/activities/{quote(activity)}/participants?email={quote(email)}"

    # Act
    response = client.delete(url)

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Removed {email} from {activity}"}

    activities = client.get("/activities").json()
    assert email not in activities[activity]["participants"]


def test_delete_missing_participant_returns_404(client):
    # Arrange
    activity = "Chess Club"
    email = "missing@mergington.edu"
    url = f"/activities/{quote(activity)}/participants?email={quote(email)}"

    # Act
    response = client.delete(url)

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
