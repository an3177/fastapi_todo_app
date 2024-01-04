from fastapi import FastAPI, Response, APIRouter, Depends, status, HTTPException
from .. import models, schemas, utils, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

router = APIRouter(prefix="/users")

@router.post("/signup", response_model = schemas.UserBase)
def signup(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_data.email).first()
    if user:
        raise HTTPException(status_code=409, detail="Email already registered")
    signedup_user = models.User(**user_data.model_dump())
    db.add(signedup_user)
    db.commit()
    db.refresh(signedup_user)
    return signedup_user

@router.post("/login", response_model=schemas.Token)
def login_for_access_token(db:Session = Depends(get_db), form_data: OAuth2PasswordRequestForm=Depends()):
    user = utils.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password", headers={"WWW-Authetnicate": "Bearer"})
    access_token_expires = timedelta(minutes=oauth2.EXPIRE_MINUTES)
    access_token = oauth2.create_access_token(data={"email":user.email}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type":"bearer"}

@router.get("/me", response_model=schemas.UserBase)
def read_logged_in_user(current_user: models.User = Depends(oauth2.get_current_user)):
    return current_user

