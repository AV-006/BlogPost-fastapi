from fastapi import APIRouter,Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from ..database import create_session
from ..models import User
from ..hashing import password_hash,DUMMY_HASH
from ..token import ACCESS_TOKEN_EXPIRE_MINUTES,create_access_token
from ..schemas import Token

router = APIRouter(tags=['Authentication'])

#login route
@router.post('/login')
def login_user(session: Session =Depends(create_session), form_data: OAuth2PasswordRequestForm = Depends()):
    user=session.query(User).filter(form_data.username==User.email).first()
    if not user:
        password_hash.verify(form_data.password,DUMMY_HASH)
        return {"message": "Invalid login credentials"} 
    if not password_hash.verify(form_data.password,user.password):
        return {"message": "Invalid login credentials"}
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")