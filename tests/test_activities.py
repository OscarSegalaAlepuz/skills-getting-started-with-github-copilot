"""Tests for Mergington High School API activities endpoints."""

import pytest


class TestGetActivities:
    """Test GET /activities endpoint."""

    def test_get_activities_success(self, client):
        """Test successful retrieval of all activities."""
        # Arrange: No special setup needed as activities are in-memory

        # Act: Make GET request to /activities
        response = client.get("/activities")

        # Assert: Check response status and structure
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert len(data) > 0  # Should have activities

        # Check structure of first activity
        first_activity = next(iter(data.values()))
        assert "description" in first_activity
        assert "schedule" in first_activity
        assert "max_participants" in first_activity
        assert "participants" in first_activity
        assert isinstance(first_activity["participants"], list)


class TestSignupForActivity:
    """Test POST /activities/{activity_name}/signup endpoint."""

    def test_signup_success(self, client):
        """Test successful signup for an activity."""
        # Arrange: Use an existing activity and new email
        activity_name = "Chess Club"
        email = "newstudent@mergington.edu"

        # Act: Make POST request to signup
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert: Check success response
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]

    def test_signup_activity_not_found(self, client):
        """Test signup for non-existent activity."""
        # Arrange: Use non-existent activity name
        activity_name = "NonExistentActivity"
        email = "student@mergington.edu"

        # Act: Make POST request to signup
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert: Check 404 response
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "Activity not found" in data["detail"]

    def test_signup_duplicate_email(self, client):
        """Test signup with email already registered."""
        # Arrange: Use existing participant email
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already in participants

        # Act: Make POST request to signup
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert: Check 400 response for duplicate
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "already signed up" in data["detail"]


class TestRemoveParticipant:
    """Test DELETE /activities/{activity_name}/participants endpoint."""

    def test_remove_participant_success(self, client):
        """Test successful removal of a participant."""
        # Arrange: Use existing participant
        activity_name = "Programming Class"
        email = "emma@mergington.edu"  # Already in participants

        # Act: Make DELETE request to remove participant
        response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email}
        )

        # Assert: Check success response
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]

    def test_remove_participant_activity_not_found(self, client):
        """Test removal from non-existent activity."""
        # Arrange: Use non-existent activity
        activity_name = "NonExistentActivity"
        email = "student@mergington.edu"

        # Act: Make DELETE request
        response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email}
        )

        # Assert: Check 404 response
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "Activity not found" in data["detail"]

    def test_remove_participant_not_found(self, client):
        """Test removal of non-existent participant."""
        # Arrange: Use valid activity but email not in participants
        activity_name = "Chess Club"
        email = "nonexistent@mergington.edu"

        # Act: Make DELETE request
        response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email}
        )

        # Assert: Check 404 response
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "Participant not found" in data["detail"]


class TestRootRedirect:
    """Test GET / root endpoint redirect."""

    def test_root_redirect(self, client):
        """Test that root endpoint redirects to static index."""
        # Arrange: No special setup

        # Act: Make GET request to root
        response = client.get("/", follow_redirects=False)

        # Assert: Check redirect response
        assert response.status_code == 307  # Temporary redirect
        assert response.headers["location"] == "/static/index.html"