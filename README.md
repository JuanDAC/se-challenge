# User Management API 👤

## Overview

This project provides a robust and scalable RESTful API for managing user data. It implements complete CRUD (Create, Read, Update, Delete) operations for users, each identified by a unique ID. The API is designed following principles of clean architecture to ensure separation of concerns, testability, and maintainability.

## Features ✨

-   **Complete User CRUD:** Full support for creating, reading, updating, and deleting user records.
-   **User Attributes:** Manages users with attributes including `id`, `username`, `email`, `first_name`, `last_name`, `role`, `created_at`, `updated_at`, and `active` status.
-   **Unique Constraints:** Ensures data integrity with unique constraints on fields like `email`.
-   **Request Validation:** Validates incoming requests to ensure data correctness and prevent invalid states (e.g., invalid email format, missing required fields).
-   **Error Handling:** Provides informative error responses for invalid requests (e.g., 400 Bad Request, 422 Unprocessable Entity) and resource not found scenarios (e.g., 404 Not Found).
-   **Pagination Support:** Supports listing users with pagination parameters (`skip`, `limit`).
-   **Filtering:** Allows filtering users based on attributes like `active` status.
-   **Automated Testing:** Includes Postman collection for API functional and failure tests.

## Core Use Cases

-   **Create User:** Register a new user with specified details.
-   **Retrieve User:** Fetch details of a specific user by their unique ID.
-   **List Users:** Retrieve a paginated and filterable list of all users.
-   **Update User:** Modify the details of an existing user.
-   **Delete User:** Remove a user record from the system.

## Getting Started 🚀

### Prerequisites

-   Python 3.11+
-   PostgreSQL 13+

### Configuration

Create a `.env` file in the project root directory based on the provided template. Do **not** expose sensitive credentials.

```ini
# Database Configuration
DB_HOST=
DB_PORT=
DB_DATABASE_NAME=
DB_USER=
DB_PASSWORD=
DB_DIALECT=
DB_SCHEMA=

# API Configuration
API_HOST=
API_PORT=
DEBUG=

# Other Configurations
SECRET_KEY=
APP_NAME=
API_VERSION=
````

Fill in the appropriate values for your environment.

## API Endpoints

The API provides the following endpoints under the base path `/api/v1/`:

  - **`POST /users/`**: Create a new user.
  - **`GET /users/{user_id}`**: Retrieve a specific user by ID.
  - **`GET /users/`**: List users. Supports query parameters `skip`, `limit`, and `active`.
  - **`PUT /users/{user_id}`**: Update a specific user by ID.
  - **`DELETE /users/{user_id}`**: Delete a specific user by ID.

Refer to the included Postman collection (`postman/User Management API - CRUD Tests.json`) for detailed request/response examples and test cases.

## Architecture

The project follows a Clean Architecture or Hexagonal Architecture pattern, promoting separation of concerns and dependency inversion.

### Core Components

```mermaid
graph TD
    A[Presentation: HTTP/CLI] --> B[Use Cases]
    B --> C[Ports: Interfaces]
    C --> D[Infrastructure: Adapters]
    D --> E[Domain: Entities/Value Objects]
    Subgraph Application
        B
        C
    End
    Subgraph External
        A
        D
        E
    End
```

  * **Domain:** Contains the core business logic, entities, and value objects, independent of infrastructure details.
  * **Use Cases:** Encapsulate application-specific business rules and orchestrate the flow between the presentation layer and the domain/infrastructure.
  * **Ports:** Define interfaces (abstractions) that the use cases depend on. These represent the contracts for interacting with external services (like databases or external APIs).
  * **Infrastructure:** Contains the implementation details (adapters) that fulfill the contracts defined in the ports. This includes database repositories, external service clients, etc.
  * **Presentation:** Handles user interaction, such as the HTTP API or a Command Line Interface (CLI). It translates external requests into inputs for the use cases and formats the output from the use cases into appropriate responses.

## Environment Variables

The application uses environment variables for configuration. A `.env` file is used to load these variables during local development. Key variables include:

  - `DB_HOST`: Database host.
  - `DB_PORT`: Database port.
  - `DB_DATABASE_NAME`: Name of the database.
  - `DB_USER`: Database username.
  - `DB_PASSWORD`: Database password.
  - `DB_DIALECT`: Database dialect (e.g., `postgresql`).
  - `DB_SCHEMA`: Database schema.
  - `API_HOST`: Host address for the API.
  - `API_PORT`: Port for the API.
  - `DEBUG`: Boolean flag for debug mode.
  - `SECRET_KEY`: Secret key for security purposes.
  - `APP_NAME`: Application name.
  - `API_VERSION`: API version.

## Docker

You can build and run the application using Docker:

```bash
docker build -t user-management-api .
docker run -p 8000:8000 --env-file .env user-management-api
```

Ensure you have a `.env` file configured for the Docker container to access the database and set other configurations.

## Contributing

1.  Clone the repository: `git clone <repository_url>`
2.  Create feature branch: (`git checkout -b feature/your-feature-name`)
3.  Commit changes: (`git commit -am ':sparkles: Add your feature'`)
4.  Push to branch: (`git push origin feature/your-feature-name`)
5.  Open a Pull Request

-----

**Project Status**: Active Development 🚧

