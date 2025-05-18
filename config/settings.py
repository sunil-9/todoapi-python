"""
Configuration settings for the application.
Contains all credentials and environment variables.
"""
from typing import Dict, Any

# Database configurations
DATABASE_CONFIG = {
    "host": "localhost",
    "username": "root",
    "password": "",
    "database": "todoapp"
}

# Email configurations for sending OTP
EMAIL_CONFIG = {
    "email": "",  # Add your email here
    "password": ""  # Add your app password here
}

# JWT configurations for authentication
JWT_SECRET_KEY = "your-secret-key-for-jwt-tokens"
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_MINUTES = 30

# Other application settings
APP_NAME = "Todo API"
APP_VERSION = "1.0.0"
