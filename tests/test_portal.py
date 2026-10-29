
import pytest

from app import app, submissions


@pytest.fixture
def client():
    app.config["TESTING"] = True
    submissions.clear()

    with app.test_client() as test_client:
        yield test_client

    submissions.clear()


def test_valid_submission_is_saved(client):
    response = client.post(
        "/",
        data={
            "student_name": "Ali Ahmed",
            "registration_number": "FA23-BSE-001",
            "assignment_title": "Cloud Computing Lab",
            "submission_url": "https://example.com/assignment",
        },
    )

    assert response.status_code == 200
    assert b"Assignment submitted successfully!" in response.data
    assert len(submissions) == 1
    assert submissions[0]["student_name"] == "Ali Ahmed"


def test_missing_registration_number_is_rejected(client):
    response = client.post(
        "/",
        data={
            "student_name": "Ali Ahmed",
            "registration_number": "",
            "assignment_title": "Cloud Computing Lab",
            "submission_url": "https://example.com/assignment",
        },
    )

    assert response.status_code == 200
    assert b"All fields are required" in response.data
    assert len(submissions) == 0


def test_invalid_submission_url_is_rejected(client):
    response = client.post(
        "/",
        data={
            "student_name": "Ali Ahmed",
            "registration_number": "FA23-BSE-001",
            "assignment_title": "Cloud Computing Lab",
            "submission_url": "not-a-valid-url",
        },
    )

    assert response.status_code == 200
    assert b"valid HTTP or HTTPS URL" in response.data
    assert len(submissions) == 0

