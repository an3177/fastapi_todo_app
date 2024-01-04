from fastapi import FastAPI, Response, APIRouter, Depends, status, HTTPException
from .. import models, schemas, utils, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from typing import List

router = APIRouter(prefix="/todos")

@router.get("/mytodos", response_model = List[schemas.TODOResponse])
def get_my_todo_view(db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    todos = db.query(models.TODO). filter(models.TODO.owner == current_user).all()
    return todos

@router.post("/mytodos", response_model = schemas.TODOResponse)
def add_todo_view(todo_data : schemas.TODOBase, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    new_todo = models.TODO(owner_id = current_user.id, **todo_data.model_dump())
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo

@router.put("/{id}", response_model = schemas.TODOResponse)
def update_todo(id:int, todo_data: schemas.TODOBase, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    todos = db.query(models.TODO).filter(models.TODO.id == id)
    updated_todo = todos.first()
    if updated_todo == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"todo with id: {id} does not exist")
    if updated_todo.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    todos.update(todo_data.model_dump(), synchronize_session= False)
    db.commit()
    return todos.first()

@router.delete("/{id}", response_model= schemas.TODOResponse)
def delete_todo(id:int, current_user: models.User = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    deleted_todo = db.query(models.TODO).filter(models.TODO.id == id).first()
    db.delete(deleted_todo)
    db.commit()





