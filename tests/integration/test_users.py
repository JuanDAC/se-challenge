import uuid
from datetime import datetime
from faker import Faker

faker = Faker()

# Valid roles defined in the schema
VALID_ROLES = ["admin", "user", "guest"]

def is_valid_uuid(val):
    try:
        uuid.UUID(str(val))
        return True
    except ValueError:
        return False

def is_iso_datetime(date_string):
    try:
        datetime.fromisoformat(date_string.replace("Z", "+00:00"))
        return True
    except (ValueError, TypeError):
        return False

class TestUserCRUD:

    def test_create_user_successfully(self, client, unique_user_payload):
        # GIVEN: A valid user payload
        payload = unique_user_payload
        
        # WHEN: A POST request is made to /users/
        response = client.post("/users/", json=payload)
        
        # THEN: The response status code should be 201 (Created)
        assert response.status_code == 201
        
        # AND: The response body should contain the new user's details
        data = response.json()
        assert data["username"] == payload["username"]
        assert data["email"] == payload["email"]
        assert data["first_name"] == payload["first_name"]
        assert data["last_name"] == payload["last_name"]
        assert data["role"] == payload["role"]
        assert data["active"] is True  # Default
        
        # AND: The ID should be a valid UUID
        assert "id" in data
        assert is_valid_uuid(data["id"])
        
        # AND: created_at and updated_at should be valid ISO timestamps
        assert "created_at" in data
        assert is_iso_datetime(data["created_at"])
        assert "updated_at" in data
        assert is_iso_datetime(data["updated_at"])
        assert data["created_at"] == data["updated_at"] # On creation, should be equal

    def test_create_user_duplicate_username(self, client, unique_user_payload):
        # GIVEN: A user already exists with a specific username
        payload1 = unique_user_payload
        response1 = client.post("/users/", json=payload1)
        assert response1.status_code == 201
        
        # AND: New user data with the same username but different email
        payload2 = {
            "username": payload1["username"], # Same username
            "email": faker.email(),
            "first_name": "Jane",
            "last_name": "Doe",
            "role": "user"
        }
        
        # WHEN: A POST request is made to /users/ with duplicate data
        response2 = client.post("/users/", json=payload2)
        
        # THEN: The status code should be 400 or 409 (depends on implementation)
        assert response2.status_code in [400, 409] 
        # AND: The response body should indicate a duplicate username error
        assert "detail" in response2.json()
        # (The exact detail message will depend on your error handling implementation)

    def test_create_user_duplicate_email(self, client, unique_user_payload):
        # GIVEN: A user already exists with a specific email
        payload1 = unique_user_payload
        response1 = client.post("/users/", json=payload1)
        assert response1.status_code == 201
        
        # AND: New user data with the same email but different username
        payload2 = {
            "username": faker.user_name(),
            "email": payload1["email"], # Same email
            "first_name": "John",
            "last_name": "Smith",
            "role": "admin"
        }
        
        # WHEN: A POST request is made to /users/ with duplicate data
        response2 = client.post("/users/", json=payload2)
        
        # THEN: The status code should be 400 or 409
        assert response2.status_code in [400, 409]
        # AND: The response body should indicate a duplicate email error
        assert "detail" in response2.json()

    def test_create_user_missing_required_fields(self, client):
        # GIVEN: User data with missing required fields (e.g., username)
        payload = {
            # "username": "missinguser", # Missing field
            "email": faker.email(),
            "first_name": "Missing",
            "last_name": "Fields",
            "role": "guest"
        }
        
        # WHEN: A POST request is made to /users/
        response = client.post("/users/", json=payload)
        
        # THEN: The status code should be 422 (Unprocessable Entity)
        assert response.status_code == 422
        # AND: The response body should detail the validation error
        error_data = response.json()
        assert "detail" in error_data
        assert any(err["loc"] == ["body", "username"] and err["type"] == "missing" for err in error_data["detail"])


    def test_create_user_invalid_email_format(self, client, unique_user_payload):
        # GIVEN: User data with an invalid email format
        payload = unique_user_payload
        payload["email"] = "not-an-email"
        
        # WHEN: A POST request is made to /users/
        response = client.post("/users/", json=payload)
        
        # THEN: The status code should be 422
        assert response.status_code == 422
        # AND: The response body should detail the validation error for email
        error_data = response.json()
        assert "detail" in error_data
        assert any(err["loc"] == ["body", "email"] for err in error_data["detail"])

    def test_create_user_invalid_role(self, client, unique_user_payload):
        # GIVEN: User data with an invalid role
        payload = unique_user_payload
        payload["role"] = "invalid_role"
        
        # WHEN: A POST request is made to /users/
        response = client.post("/users/", json=payload)
        
        # THEN: The status code should be 422
        assert response.status_code == 422
        # AND: The response body should detail the validation error for role
        error_data = response.json()
        assert "detail" in error_data
        assert any(err["loc"] == ["body", "role"] for err in error_data["detail"])

    def test_get_user_by_id_successfully(self, client, created_user):
        # GIVEN: A user exists in the system (using the created_user fixture)
        user_id = created_user["id"]
        
        # WHEN: A GET request is made to /users/{user_id}
        response = client.get(f"/users/{user_id}")
        
        # THEN: The status code should be 200 (OK)
        assert response.status_code == 200
        
        # AND: The response body should contain the correct user details
        data = response.json()
        assert data["id"] == user_id
        assert data["username"] == created_user["username"]
        assert data["email"] == created_user["email"]

    def test_get_user_by_id_not_found(self, client):
        # GIVEN: A user ID that does not exist
        non_existent_uuid = str(uuid.uuid4())
        
        # WHEN: A GET request is made to /users/{non_existent_uuid}
        response = client.get(f"/users/{non_existent_uuid}")
        
        # THEN: The status code should be 404 (Not Found)
        assert response.status_code == 404
        assert "detail" in response.json() # For example: "User not found"

    def test_get_user_by_id_invalid_uuid_format(self, client):
        # GIVEN: A user ID with invalid format
        invalid_user_id = "not-a-uuid"
        
        # WHEN: A GET request is made to /users/{invalid_user_id}
        response = client.get(f"/users/{invalid_user_id}")
        
        # THEN: The status code should be 422 (Unprocessable Entity)
        assert response.status_code == 422 # FastAPI handles this for typed path parameters

    def test_get_all_users(self, client, created_user):
        # GIVEN: At least one user exists in the system
        # (the created_user fixture has already created one)
        # Optionally, create more users if needed to test the list
        # client.post("/users/", json=unique_user_payload_generator())

        # WHEN: A GET request is made to /users/
        response = client.get("/users/")
        
        # THEN: The status code should be 200 (OK)
        assert response.status_code == 200
        
        # AND: The response body should be a list
        data = response.json()
        assert isinstance(data, list)
        
        # AND: The list should contain at least the created user
        assert len(data) >= 1
        assert any(user["id"] == created_user["id"] for user in data)

    def test_update_user_successfully(self, client, created_user):
        # GIVEN: An existing user
        user_id = created_user["id"]
        original_updated_at = created_user["updated_at"]
        
        # AND: Valid data to update the user
        update_payload = {
            "first_name": "Updated First Name",
            "last_name": "Updated Last Name",
            "role": "admin",
            "active": False
        }
        
        # WHEN: A PUT request is made to /users/{user_id} with update data
        response = client.put(f"/users/{user_id}", json=update_payload)
        
        # THEN: The status code should be 200 (OK)
        assert response.status_code == 200
        
        # AND: The response body should contain the updated user details
        data = response.json()
        assert data["id"] == user_id
        assert data["first_name"] == update_payload["first_name"]
        assert data["last_name"] == update_payload["last_name"]
        assert data["role"] == update_payload["role"]
        assert data["active"] == update_payload["active"]
        assert data["username"] == created_user["username"]
        
        # AND: The updated_at timestamp should be more recent than the original
        assert "updated_at" in data
        assert is_iso_datetime(data["updated_at"])
        assert datetime.fromisoformat(data["updated_at"].replace("Z", "+00:00")) > datetime.fromisoformat(original_updated_at.replace("Z", "+00:00"))

    def test_update_user_partially(self, client, created_user):
        # GIVEN: An existing user
        user_id = created_user["id"]
        
        # AND: Partial data to update (only first_name)
        update_payload = {"first_name": "Partial Update Name"}
        
        # WHEN: A PUT request is made to /users/{user_id}
        response = client.put(f"/users/{user_id}", json=update_payload)
        
        # THEN: The status code should be 200 (OK)
        assert response.status_code == 200
        data = response.json()
        assert data["first_name"] == update_payload["first_name"]
        assert data["last_name"] == created_user["last_name"]

    def test_update_user_not_found(self, client):
        # GIVEN: A user ID that does not exist
        non_existent_uuid = str(uuid.uuid4())
        update_payload = {"first_name": "Ghost User"}
        
        # WHEN: A PUT request is made to /users/{non_existent_uuid}
        response = client.put(f"/users/{non_existent_uuid}", json=update_payload)
        
        # THEN: The status code should be 404 (Not Found)
        assert response.status_code == 404

    def test_update_user_invalid_data(self, client, created_user):
        # GIVEN: An existing user
        user_id = created_user["id"]
        
        # AND: Update data with an invalid email format
        update_payload = {"email": "not-a-valid-email"}
        
        # WHEN: A PUT request is made to /users/{user_id}
        response = client.put(f"/users/{user_id}", json=update_payload)
        
        # THEN: The status code should be 422 (Unprocessable Entity)
        assert response.status_code == 422
        error_data = response.json()
        assert any(err["loc"] == ["body", "email"] for err in error_data["detail"])

    def test_update_user_username_to_existing_one(self, client, unique_user_payload):
        # GIVEN: Two existing users, User A and User B
        user_a_payload = unique_user_payload
        response_a = client.post("/users/", json=user_a_payload)
        assert response_a.status_code == 201
        user_a_id = response_a.json()["id"]
        
        user_b_payload = { # Generate another different payload
            "username": faker.user_name() + str(uuid.uuid4())[:4],
            "email": faker.email() + str(uuid.uuid4())[:4],
            "first_name": faker.first_name(), "last_name": faker.last_name(), "role": "user"
        }
        response_b = client.post("/users/", json=user_b_payload)
        assert response_b.status_code == 201
        user_b_username = response_b.json()["username"]

        # AND: Update data for User A to change their username to User B's username
        update_payload_for_a = {"username": user_b_username}
        
        # WHEN: A PUT request is made to update User A
        response_update_a = client.put(f"/users/{user_a_id}", json=update_payload_for_a)
        
        # THEN: The status code should be 400 or 409 (conflict)
        assert response_update_a.status_code in [400, 409]

    def test_delete_user_successfully(self, client, unique_user_payload):
        # GIVEN: An existing user to be deleted
        # (create one specifically for this test to avoid relying on the `created_user` fixture
        # which could have side effects if using `yield` and then deleting here)
        payload = unique_user_payload
        create_response = client.post("/users/", json=payload)
        assert create_response.status_code == 201
        user_id_to_delete = create_response.json()["id"]
        
        # WHEN: A DELETE request is made to /users/{user_id_to_delete}
        delete_response = client.delete(f"/users/{user_id_to_delete}")
        
        # THEN: The status code should be 200 (OK) or 204 (No Content)
        assert delete_response.status_code in [200, 204]
        
        # AND (Optional, if 200 and returns the object): The body may contain the deleted user's data
        if delete_response.status_code == 200:
            assert delete_response.json()["id"] == user_id_to_delete

        # VERIFY: The user can no longer be retrieved
        get_response = client.get(f"/users/{user_id_to_delete}")
        assert get_response.status_code == 404

    def test_delete_user_not_found(self, client):
        # GIVEN: A user ID that does not exist
        non_existent_uuid = str(uuid.uuid4())
        
        # WHEN: A DELETE request is made to /users/{non_existent_uuid}
        response = client.delete(f"/users/{non_existent_uuid}")
        
        # THEN: The status code should be 404 (Not Found)
        assert response.status_code == 404