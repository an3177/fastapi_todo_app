from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from datetime import timedelta, datetime
from fastapi import HTTPException, status, Depends
from . import schemas, models, database
from sqlalchemy.orm import Session
from .config import settings
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
EXPIRE_MINUTES = settings.expire_minutes

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data:dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expires = datetime.utcnow() + expires_delta
    else:
        expires = datetime.utcnow() + timedelta(EXPIRE_MINUTES)
    to_encode.update({'exp': expires})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)
    return encode_jwt

def decode_access_token(db, token):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate":"Bearer"})
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("email")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = db.query(models.User).filter(models.User.email == email).first()
    if user is None:
        raise credentials_exception
    return user

def get_current_user(db: Session = Depends(database.get_db), token: str = Depends(oauth2_scheme)):
    return decode_access_token(db, token)



