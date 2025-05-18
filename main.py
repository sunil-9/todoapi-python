from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging

from config.database import get_db, engine
from database.connection import init_db, check_connection
from routes import todo_routes, user_routes

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Todo API",
    description="A FastAPI-based Todo application with user authentication and CRUD operations",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, you should specify the allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(todo_routes.router)
app.include_router(user_routes.router)

# Root endpoint
@app.get("/")
def read_root():
    return {
        "message": "Welcome to the Todo API",
        "docs": "/docs",
        "endpoints": {
            "todos": "/todos",
            "users": "/users"
        }
    }

# Startup event
@app.on_event("startup")
async def startup_event():
    logger.info("Starting up the application...")
    
    try:
        # Check database connection
        connection_success, message = check_connection()
        logger.info(message)
        
        if connection_success:
            # Initialize database tables
            tables = init_db()
            logger.info(f"Database initialized with tables: {tables}")
        else:
            logger.warning("Database connection failed but application will continue running")
            logger.warning("API endpoints that require database access will return errors")
            logger.warning("Please ensure MySQL is running and create a database named 'todoapp'")
    except Exception as e:
        logger.error(f"Error during startup: {str(e)}")
        logger.warning("Application started with errors")
    
    logger.info("Application startup completed")


# For direct execution
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
