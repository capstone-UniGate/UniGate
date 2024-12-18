import secrets
import string
from uuid import UUID
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from unigate.main import app
from unigate.models import Student
from unigate.core.database import engine

client: TestClient = TestClient(app)

# Test user credentials (replace with real test credentials)
test_student_username = "S1234567"
test_student_password = "testpassword"
test_student_id = "d6dcf3b1-425a-4864-88d3-525decebef18"


def authenticate_user() -> dict:
    """
    Authenticate the test user and return authentication details.
    """
    login_payload = {
        "username": test_student_username,
        "password": test_student_password,
    }

    response = client.post("/auth/login", data=login_payload)

    assert response.status_code == 200, f"Failed to authenticate user: {response.json()}"
    return response.json()


def create_student(student_id: str) -> None:
    """
    Check if a Student record exists, and create one if it does not.

    Args:
        student_id (str): The UUID of the student to check or insert.
    """
    with Session(engine) as session:
        # Check if the student already exists
        existing_student = session.query(Student).filter_by(id=UUID(student_id)).first()
        if existing_student:
            return

        # Create a new student record
        student = Student(
            id=UUID(student_id),
            hashed_password="hashedpassword123",  # Replace with actual hashed password logic
            number=12345,  # Unique student number
            email="teststudent@example.com",  # Unique email
            name="Test",
            surname="Student",
        )
        session.add(student)
        session.commit()


def test_create_group_success() -> None:
    """
    Test creating a group successfully using a real student.
    """
    # Create the student and authenticate
    create_student(test_student_id)
    token_data = authenticate_user()
    token = token_data["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Prepare valid group data
    valid_group_payload = {
        "name": f"TestGroup-{''.join(secrets.choice(string.ascii_letters) for _ in range(6))}",
        "description": "A test group description",
        "category": "Test Category",
        "type": "Public",
        "creator_id": test_student_id,
    }

    # Send POST request to create the group
    response = client.post("/groups", json=valid_group_payload, headers=headers)

    # Assertions to verify the group is created
    assert response.status_code == 200, f"Expected status code 201, but got {response.status_code}"
    data = response.json()
    assert data["name"] == valid_group_payload["name"]
    assert data["description"] == valid_group_payload["description"]
    assert data["category"] == valid_group_payload["category"]
    assert data["type"] == valid_group_payload["type"]
    assert "students" in data
    assert "super_students" in data
    assert "blocked_students" in data


def test_create_group_invalid_type() -> None:
    """
    Test creating a group with an invalid type.
    """
    # Create the student and authenticate
    create_student(test_student_id)
    token_data = authenticate_user()
    token = token_data["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Prepare invalid group data
    invalid_group_payload = {
        "name": f"TestGroup-{''.join(secrets.choice(string.ascii_letters) for _ in range(6))}",
        "description": "A test group description",
        "category": "Test Category",
        "type": "InvalidType",  # Invalid type
        "creator_id": test_student_id,
    }

    # Send POST request to create the group
    response = client.post("/groups", json=invalid_group_payload, headers=headers)

    # Assertions to check if the invalid type is rejected
    assert response.status_code == 422

def test_get_group_info() -> None:
    """
    Test retrieving a group by its ID.
    """
    # Create the student and authenticate
    create_student(test_student_id)
    token_data = authenticate_user()
    token = token_data["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create a group first
    valid_group_payload = {
        "name": f"TestGroup-{''.join(secrets.choice(string.ascii_letters) for _ in range(6))}",
        "description": "A test group description",
        "category": "Test Category",
        "type": "Public",
        "creator_id": test_student_id,
    }
    create_group_response = client.post("/groups", json=valid_group_payload, headers=headers)
    created_group = create_group_response.json()

    # Now retrieve the group by its ID
    group_id = created_group["id"]
    response = client.get(f"/groups/{group_id}", headers=headers)

    # Assertions to verify the group details
    assert response.status_code == 200
    assert response.json() == created_group