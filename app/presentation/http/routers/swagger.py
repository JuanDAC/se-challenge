CREATE_USER_SWAGGER = """
## Create User

This API endpoint allows you to create a new user in the system.

### Use Case

This endpoint is used to register new users in the application. It handles the creation of user accounts with necessary details.

### Request

**Method:** `POST`

**Path:** `/users/`

**Request Body:**

The request body should be a JSON object conforming to the `UserCreateSchema`:

```json
{
  "email": "user@example.com",
  "username": "newuser",
  "password": "securepassword",
  "first_name": "John",
  "last_name": "Doe"
}
````

**Schema:** `UserCreateSchema`

| Field        | Description                                  | Required | Type     | Example           | Constraints             |
|--------------|----------------------------------------------|----------|----------|-------------------|-------------------------|
| `email`      | The email address of the user.              | Yes      | `string` | `user@example.com`| Email format            |
| `username`   | The unique username for the user.           | Yes      | `string` | `newuser`         | Minimum length: 3, Maximum length: 50 |
| `password`   | The user's password.                         | Yes      | `string` | `securepassword`  |                         |
| `first_name` | The first name of the user.                | Yes      | `string` | `John`            |                         |
| `last_name`  | The last name of the user.                 | Yes      | `string` | `Doe`             |                         |

### Response

#### Successful Response (`201 Created`)

A successful response indicates that the user was created successfully. The response body contains the details of the newly created user.

**Response Body:**

```json
{
  "id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
  "email": "user@example.com",
  "username": "newuser",
  "first_name": "John",
  "last_name": "Doe",
  "active": true,
  "role": "user",
  "created_at": "2025-05-15T02:05:00.000Z",
  "updated_at": "2025-05-15T02:05:00.000Z"
}
```

**Schema:** `UserResponseSchema`

| Field        | Description                          | Type     | Example                             |
|--------------|--------------------------------------|----------|-------------------------------------|
| `id`         | The unique ID of the user.           | `string` | `a1b2c3d4-e5f6-7890-1234-567890abcdef` |
| `email`      | The email address of the user.       | `string` | `user@example.com`                |
| `username`   | The username of the user.            | `string` | `newuser`                           |
| `first_name` | The first name of the user.          | `string` | `John`                              |
| `last_name`  | The last name of the user.           | `string` | `Doe`                               |
| `active`     | The activation status of the user.   | `boolean`| `true`                              |
| `role`       | The role of the user.                | `string` | `user`                              |
| `created_at` | The timestamp of user creation.      | `string` | `2025-05-15T02:05:00.000Z`          |
| `updated_at` | The timestamp of the last update.    | `string` | `2025-05-15T02:05:00.000Z`          |

#### Error Responses

| Status Code           | Description                                                                 | Example Response                                      |
|-----------------------|-----------------------------------------------------------------------------|-------------------------------------------------------|
| `400 Bad Request`     | The username or email is already registered, or the request body is invalid. | `{"detail": "Email already registered."}` or `{"detail": "Username already taken."}` |
| `500 Internal Server Error` | An unexpected error occurred during user creation.                      | `{"detail": "Error al crear el usuario"}`             |
"""

GET_USER_SWAGGER = """

## Get User by ID

This API endpoint allows you to retrieve the details of a specific user based on their unique ID.

### Use Case

This endpoint is used to fetch the information of a particular user when their ID is known.

### Request

**Method:** `GET`

**Path:** `/users/{user_id}`

**Path Parameters:**

| Parameter  | Description                      | Required | Type     | Example                             |
|------------|----------------------------------|----------|----------|-------------------------------------|
| `user_id`  | The unique ID of the user.       | Yes      | `string` | `a1b2c3d4-e5f6-7890-1234-567890abcdef` |

### Response

#### Successful Response (`200 OK`)

A successful response contains the details of the requested user.

**Response Body:** (See `UserResponseSchema` in Create User documentation)

#### Error Response

| Status Code           | Description                                          | Example Response                  |
|-----------------------|------------------------------------------------------|-----------------------------------|
| `404 Not Found`       | No user found with the specified ID.               | `{"detail": "Usuario no encontrado"}` |
"""

LIST_USERS_SWAGGER = """

## List Users

This API endpoint allows you to retrieve a list of users, with support for pagination and filtering.

### Use Case

This endpoint is used to fetch multiple user records, optionally allowing you to control the number of results and filter based on their active status.

### Request

**Method:** `GET`

**Path:** `/users/`

**Query Parameters:**

| Parameter | Description                                  | Required | Type    | Default | Example |
|-----------|----------------------------------------------|----------|---------|---------|---------|
| `skip`    | Number of users to skip for pagination.      | No       | `integer`| `0`     | `10`    |
| `limit`   | Maximum number of users to return.         | No       | `integer`| `100`   | `50`    |
| `active`  | Filter users by their active status.         | No       | `boolean`| `None`  | `true`  |

### Response

#### Successful Response (`200 OK`)

A successful response contains a list of user objects.

**Response Body:**

```json
[
  {
    "id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
    "email": "user1@example.com",
    "username": "user1",
    "first_name": "John",
    "last_name": "Doe",
    "active": true,
    "role": "user",
    "created_at": "2025-05-15T02:05:00.000Z",
    "updated_at": "2025-05-15T02:05:00.000Z"
  },
  {
    "id": "f9e8d7c6-b5a4-3210-fedc-ba9876543210",
    "email": "user2@example.com",
    "username": "user2",
    "first_name": "Jane",
    "last_name": "Smith",
    "active": false,
    "role": "user",
    "created_at": "2025-05-15T02:06:00.000Z",
    "updated_at": "2025-05-15T02:06:00.000Z"
  }
]
```

**Schema:** `List[UserResponseSchema]`

#### Error Response

This endpoint typically returns `200 OK` even if no users match the criteria (in which case an empty list is returned). Server errors might result in a `500 Internal Server Error`.
"""

UPDATE_USER_SWAGGER = """

## Update User by ID

This API endpoint allows you to update the information of an existing user identified by their unique ID.

### Use Case

This endpoint is used to modify the details of a user, such as their name or active status.

### Request

**Method:** `PUT`

**Path:** `/users/{user_id}`

**Path Parameters:**

| Parameter  | Description                      | Required | Type     | Example                             |
|------------|----------------------------------|----------|----------|-------------------------------------|
| `user_id`  | The unique ID of the user to update.| Yes      | `string` | `a1b2c3d4-e5f6-7890-1234-567890abcdef` |

**Request Body:**

The request body should be a JSON object conforming to the `UserUpdateSchema`. Only the fields you want to update need to be included.

```json
{
  "first_name": "Johnny",
  "active": false
}
```

**Schema:** `UserUpdateSchema`

| Field        | Description                          | Required | Type     | Example   |
|--------------|--------------------------------------|----------|----------|-----------|
| `email`      | (Optional) The email address.        | No       | `string` | `new@example.com` |
| `username`   | (Optional) The username.             | No       | `string` | `newusername`     |
| `first_name` | (Optional) The first name.           | No       | `string` | `Johnny`  |
| `last_name`  | (Optional) The last name.            | No       | `string` | `Doe Jr.` |
| `active`     | (Optional) The activation status.    | No       | `boolean`| `false`   |
| `password`   | (Optional) The new password.         | No       | `string` | `newsecurepassword`|

### Response

#### Successful Response (`200 OK`)

A successful response contains the details of the updated user.

**Response Body:** (See `UserResponseSchema` in Create User documentation)

#### Error Response

| Status Code           | Description                                          | Example Response                  |
|-----------------------|------------------------------------------------------|-----------------------------------|
| `404 Not Found`       | No user found with the specified ID.               | `{"detail": "Usuario no encontrado"}` |
"""

DELETE_USER_SWAGGER = """

## Delete User by ID

This API endpoint allows you to delete a user from the system based on their unique ID.

### Use Case

This endpoint is used to permanently remove a user account from the application.

### Request

**Method:** `DELETE`

**Path:** `/users/{user_id}`

**Path Parameters:**

| Parameter  | Description                      | Required | Type     | Example                             |
|------------|----------------------------------|----------|----------|-------------------------------------|
| `user_id`  | The unique ID of the user to delete. | Yes      | `string` | `a1b2c3d4-e5f6-7890-1234-567890abcdef` |

### Response

#### Successful Response (`204 No Content`)

A successful response indicates that the user was deleted successfully. There is no response body for this status code.

#### Error Response

| Status Code           | Description                                          | Example Response                  |
|-----------------------|------------------------------------------------------|-----------------------------------|
| `404 Not Found`       | No user found with the specified ID.               | `{"detail": "Usuario no encontrado"}` |
"""
