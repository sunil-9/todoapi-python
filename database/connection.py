"""
Database connection utilities and initialization.
"""
import logging
from sqlalchemy import inspect
from config.database import engine, Base
from models.todo import Todo
from models.user import User

# Set up logging
logger = logging.getLogger(__name__)

def init_db():
    """
    Initialize the database, creating tables if they don't exist.
    """
    try:
        # Create tables if they don't exist
        Base.metadata.create_all(bind=engine)
        
        # Log tables that were created
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        logger.info(f"Database initialized with tables: {tables}")
        
        return tables
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}")
        logger.warning("Application will run, but database functionality will be limited")
        return []

def check_connection():
    """
    Check if database connection is working properly.
    """
    try:
        # Try to connect and execute a simple query
        connection = engine.connect()
        connection.close()
        return True, "Database connection successful"
    except Exception as e:
        error_msg = f"Database connection failed: {str(e)}"
        logger.error(error_msg)
        logger.warning("Make sure MySQL is running and a database 'todoapp' exists")
        logger.warning("Use MySQL command: CREATE DATABASE todoapp;")
        return False, error_msg
