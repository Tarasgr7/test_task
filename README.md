# Project Documentation

This is a **FastAPI-based** project that handles posts, user authentication, and integrates Redis for caching. The project utilizes **MySQL** for persistent data storage and **Redis** for caching responses related to posts.

## Project Structure

```
.
├── app
│   ├── models
│   │   └── post_model.py
│   ├── schemas
│   │   └── post_schemas.py
│   ├── service
│   │   └── redis_client.py
│   ├── utils
│   │   └── utils.py
│   │   └── user_utils.py
│   ├── dependencies.py
│   ├── main.py
│   └── routers
│       ├── post_router.py
│       └── user_router.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Overview

This FastAPI application includes the following main functionalities:

1. **User Management**:
    - User registration
    - User login and authentication (JWT-based)
    - Password hashing
    - JWT token creation and validation

2. **Posts Management**:
    - Creating new posts
    - Retrieving posts (with Redis caching)
    - Deleting posts
    
3. **Redis Integration**:
    - Caching posts data to improve performance (using Redis).

4. **MySQL Integration**:
    - Storing posts in a MySQL database.
    - User data and posts are persisted in MySQL.

## Requirements

To run the project locally, you need the following:

1. Python 3.8+
2. Docker (for running MySQL and Redis in containers)
3. Redis and MySQL should be available as services (dockerized).

### Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd <project-directory>
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Build and run the project using Docker:

   ```bash
   docker-compose up --build
   ```

4. After the containers are up, the FastAPI app will be accessible at `http://localhost:8000`.

## API Documentation

### Users

#### Register User

**Endpoint**: `POST /api/v1/users/register`

**Description**: Registers a new user with the given email and password.

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response**:
```json
{
  "access_token": "JWT_ACCESS_TOKEN",
  "token_type": "bearer"
}
```

**Status Codes**:
- 201: User registered successfully
- 400: User already exists

#### Login User

**Endpoint**: `POST /api/v1/users/login`

**Description**: Logs in an existing user using email and password, returns a JWT access token.

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response**:
```json
{
  "access_token": "JWT_ACCESS_TOKEN",
  "token_type": "bearer"
}
```

**Status Codes**:
- 200: Login successful
- 404: User not found

---

### Posts

#### Add Post

**Endpoint**: `POST /api/v1/posts/add-post`

**Description**: Adds a new post to the database with the specified text content. Requires authentication.

**Request Body**:
```json
{
  "text": "This is a post text"
}
```

**Response**:
```json
{
  "PostID": 1,
  "detail": "Post created"
}
```

**Status Codes**:
- 200: Post created successfully
- 401: Unauthorized (if the user is not authenticated)
- 413: Text size exceeds 1MB

---

#### Get Posts

**Endpoint**: `GET /api/v1/posts/get-posts`

**Description**: Retrieves all posts for the currently authenticated user. Cached data is used if available in Redis.

**Response**:
```json
[
  {
    "id": 1,
    "text": "This is a post text"
  },
  {
    "id": 2,
    "text": "Another post text"
  }
]
```

**Status Codes**:
- 200: Posts retrieved successfully
- 401: Unauthorized (if the user is not authenticated)

---

#### Delete Post

**Endpoint**: `DELETE /api/v1/posts/delete-post/{post_id}`

**Description**: Deletes a post by its ID. Requires authentication and that the post belongs to the authenticated user.

**Response**: 
- No content (204)

**Status Codes**:
- 204: Post deleted successfully
- 401: Unauthorized (if the user is not authenticated)
- 404: Post not found

## Dependencies

This project uses the following libraries and tools:

- **FastAPI**: Framework for building APIs with Python 3.8+.
- **SQLAlchemy**: ORM for interacting with the MySQL database.
- **Redis**: In-memory data structure store for caching.
- **PyMySQL**: MySQL driver for Python.
- **passlib**: Library for password hashing.
- **python-jose**: Library for handling JWT (JSON Web Tokens).
- **Docker**: For containerization of MySQL, Redis, and FastAPI application.

## Docker Setup

The project includes a **Docker Compose** file to easily spin up the necessary services (MySQL, Redis, and FastAPI):

1. **MySQL**: Runs MySQL 8.0 and stores the user and post data.
2. **Redis**: Provides caching for posts data.
3. **FastAPI**: The main application that exposes the API for managing users and posts.

Run the following command to build and start all services:
```bash
docker-compose up --build
```

The services will be available as follows:
- FastAPI app: `http://localhost:8000`
- MySQL: `localhost:3306`
- Redis: `localhost:6379`

## Utility Functions

### JWT Authentication and Authorization
- **`create_access_token`**: Creates a JWT token for the user with an expiration time.
- **`decode_access_token`**: Decodes a JWT token and returns the payload.
- **`authenticate_user`**: Authenticates a user by email and password.
- **`verify_password`**: Verifies the password against the hashed password stored in the database.
- **`hash_password`**: Hashes a plain password using `bcrypt`.

### Redis Client

- **`get_redis`**: Retrieves the Redis client instance to interact with the Redis server.

### Database Dependency

- **`get_db`**: Provides a SQLAlchemy session for the database interactions.
- **`db_dependency`**: Dependency that allows route functions to get the database session.
- **`user_dependency`**: Dependency that retrieves the authenticated user from the JWT token.

## Error Handling

- **401 Unauthorized**: Raised when the user is not authenticated.
- **404 Not Found**: Raised when a resource (e.g., post or user) is not found.
- **413 Request Entity Too Large**: Raised when the uploaded data exceeds the allowed size (1MB for post text).

## Conclusion

This FastAPI application is designed to manage user authentication, posts, and efficient caching of posts using Redis. It also incorporates secure password hashing and JWT-based token authentication for protecting endpoints. The integration of Redis caching ensures faster retrieval of posts, especially when the data doesn't change frequently.

For further questions or issues, please consult the [FastAPI Documentation](https://fastapi.tiangolo.com/).