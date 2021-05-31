# main.py
from fastapi import Depends, FastAPI
from fastapi import FastAPI, Path, Body, Depends
from sqlalchemy.orm import Session, sessionmaker
from starlette.requests import Request
from db import Todo, engine
 
# Connect when a session class instance for DB connection is created
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
 
# Definition of data passed to API using Pydantic Addition of Validation and Documentation functions
class TodoIn(BaseModel):
    title: str
    done: bool
 

# Utility to get a single Todo
def get_todo(db_session: Session, todo_id: int):
    return db_session.query(Todo).filter(Todo.id == todo_id).first()
 
 
# Pass the session of DB connection to the function of each endpoint
def get_db(request: Request):
    return request.state.db
 
 
# List Todo
@app.get("/todos/")
def read_todos(db: Session = Depends(get_db)):
    todos = db.query(Todo).all()
    return todos
 
 
# Get a Todo by id
@app.get("/todos/{todo_id}")
def read_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = get_todo(db, todo_id)
    return todo
 
 
# Create a Todo
@app.post("/todos/")
async def create_todo(todo_in: TodoIn, db: Session = Depends(get_db)):
    todo = Todo(title=todo_in.title, done=False)
    db.add(todo)
    db.commit()
    todo = get_todo(db, todo.id)
    return todo
 
 
# Update a Todo
@app.put("/todos/{todo_id}")
async def update_todo(todo_id: int, todo_in: TodoIn, db: Session = Depends(get_db)):
    todo = get_todo(db, todo_id)
    todo.title = todo_in.title
    todo.done = todo_in.done
    db.commit()
    todo = get_todo(db, todo_id)
    return todo
 
 
# Delete a Todo
@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = get_todo(db, todo_id)
    db.delete(todo)
    db.commit()
 
 
# Create a session instance for middleware DB connection which will be called for each request
@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request.state.db = SessionLocal()
    response = await call_next(request)
    request.state.db.close()
    return response
 