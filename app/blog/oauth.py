from sqlalchemy.orm import Session
from fastapi import Depends,HTTPException
from fastapi.security import OAuth2PasswordBearer
from .database import create_session
from .token import verify_token
from .models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str=Depends(oauth2_scheme), session: Session=Depends(create_session)):
    credentials_exception = HTTPException(
        status_code=404,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    email= verify_token(token,credentials_exception)
    user = session.query(User).filter(User.email == email).first()

    if user is None:
        raise credentials_exception

    return user