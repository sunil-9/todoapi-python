"""
Routes for Todo CRUD operations.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from config.database import get_db
from models.todo import Todo, TodoCreate, TodoUpdate, TodoResponse
from utils.auth import get_current_user

# Create router
router = APIRouter(
    prefix="/todos",
    tags=["todos"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
def create_todo(
    todo: TodoCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Create a new todo item."""
    db_todo = Todo(
        title=todo.title,
        description=todo.description,
        completed=todo.completed,
        user_id=current_user.id
    )
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

@router.get("/", response_model=List[TodoResponse])
def read_todos(
    skip: int = 0,
    limit: int = 100,
    completed: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get all todos for the current user with optional filtering."""
    query = db.query(Todo).filter(Todo.user_id == current_user.id)
    
    # Apply filter if completed status is specified
    if completed is not None:
        query = query.filter(Todo.completed == completed)
    
    # Apply pagination
    todos = query.offset(skip).limit(limit).all()
    return todos

@router.get("/{todo_id}", response_model=TodoResponse)
def read_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get a specific todo by ID."""
    db_todo = db.query(Todo).filter(
        Todo.id == todo_id,
        Todo.user_id == current_user.id
    ).first()
    
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    return db_todo

@router.put("/{todo_id}", response_model=TodoResponse)
def update_todo(
    todo_id: int,
    todo_update: TodoUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Update a todo by ID."""
    db_todo = db.query(Todo).filter(
        Todo.id == todo_id,
        Todo.user_id == current_user.id
    ).first()
    
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    # Update attributes if provided
    update_data = todo_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_todo, key, value)
    
    db.commit()
    db.refresh(db_todo)
    return db_todo

@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Delete a todo by ID."""
    db_todo = db.query(Todo).filter(
        Todo.id == todo_id,
        Todo.user_id == current_user.id
    ).first()
    
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    db.delete(db_todo)
    db.commit()
    return None

@router.put("/{todo_id}/toggle", response_model=TodoResponse)
def toggle_todo_status(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Toggle the completed status of a todo."""
    db_todo = db.query(Todo).filter(
        Todo.id == todo_id,
        Todo.user_id == current_user.id
    ).first()
    
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    # Toggle the completed status
    db_todo.completed = not db_todo.completed
    
    db.commit()
    db.refresh(db_todo)
    return db_todo
