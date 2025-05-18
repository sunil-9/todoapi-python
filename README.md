# FastAPI Todo Application

A full-featured REST API for a Todo application built with FastAPI, SQLAlchemy, and MySQL. The application includes user authentication with JWT, password reset functionality with OTP via email, and complete CRUD operations for todo items.

## Features

### User Management
- User registration with password hashing
- Login with JWT authentication
- Password reset with OTP via email

### Todo Management
- Create, read, update, and delete todos
- Filter todos by completion status
- Toggle todo completion status
- Associate todos with specific users

### Architecture
- Clean, modular architecture following FastAPI best practices
- Separate configuration, models, routes, and utilities
- Database integration with SQLAlchemy ORM
- Input validation with Pydantic

## Project Structure

```
pyapi/
├── config/              # Configuration files
│   ├── __init__.py
│   ├── database.py      # Database configuration
│   └── settings.py      # App settings and credentials
├── database/           # Database connection utilities
│   ├── __init__.py
│   └── connection.py    # DB initialization and connection checking
├── models/             # Data models
│   ├── __init__.py
│   ├── todo.py          # Todo model definition
│   └── user.py          # User and OTP models
├── routes/             # API endpoints
│   ├── __init__.py
│   ├── todo_routes.py   # Todo CRUD operations
│   └── user_routes.py   # User authentication operations
├── utils/              # Utility functions
│   ├── __init__.py
│   ├── auth.py          # Authentication utilities
│   └── email.py         # Email sending functionality
├── main.py             # Main application entry point
├── requirements.txt    # Project dependencies
├── database.sql        # SQL schema and sample data
└── README.md           # Project documentation
```

## Setup and Installation

### Prerequisites
- Python 3.10 or higher
- MySQL database server
- uv package manager

### Database Setup
1. Create a MySQL database for the application:

```sql
CREATE DATABASE todoapp;
```

2. Or use the provided `database.sql` script which includes the schema and sample data:

```bash
mysql -u root < database.sql
```

### Configuration
1. Update database connection details in `config/settings.py`
2. For email functionality, add your Gmail address and app password in `config/settings.py`
3. Configure the JWT secret key in `config/settings.py`

### Installing Dependencies
Using uv (recommended):

```bash
uv sync
```

Or using pip:

```bash
pip install -r requirements.txt
```

### Running the Application

```bash
uvicorn main:app --reload
```

The API will be available at http://localhost:8000

## API Documentation

After starting the application, you can access:
- Interactive API documentation: http://localhost:8000/docs
- Alternative documentation: http://localhost:8000/redoc

### Main Endpoints

#### User Routes
- `POST /users/register` - Register a new user
- `POST /users/login` - Login and get access token
- `GET /users/me` - Get current user info
- `POST /users/forgot-password` - Request password reset (sends OTP)
- `POST /users/verify-otp` - Verify OTP for password reset
- `POST /users/reset-password` - Reset password using OTP

#### Todo Routes
- `GET /todos` - List all todos (for authenticated user)
- `POST /todos` - Create a new todo
- `GET /todos/{todo_id}` - Get a specific todo
- `PUT /todos/{todo_id}` - Update a todo
- `DELETE /todos/{todo_id}` - Delete a todo
- `PUT /todos/{todo_id}/toggle` - Toggle completion status

## Sample Usage

### Register a New User
```bash
curl -X 'POST' \
  'http://localhost:8000/users/register' \
  -H 'Content-Type: application/json' \
  -d '{
    "email": "user@example.com",
    "username": "newuser",
    "password": "securepassword"
  }'
```

### Login
```bash
curl -X 'POST' \
  'http://localhost:8000/users/login' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'username=user@example.com&password=securepassword'
```

### Create a Todo
```bash
curl -X 'POST' \
  'http://localhost:8000/todos/' \
  -H 'Authorization: Bearer YOUR_ACCESS_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
    "title": "Learn FastAPI",
    "description": "Complete FastAPI tutorial",
    "completed": false
  }'
```

## Sample Users
The database.sql file includes these sample users (all with password 'password123'):
- user1@example.com / username: user1
- user2@example.com / username: user2
- admin@example.com / username: admin

## License
This project is licensed under the MIT License.