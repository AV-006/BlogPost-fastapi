from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from ..database import create_session
from ..models import User
from ..hashing import password_hash
from ..schemas import ShowUsers,UsersCreate
from ..oauth import get_current_user

router = APIRouter(tags=['Users'])


#user routes
@router.get('/')
def home_route():
    return {"message": "home"}

@router.get('/users/{user_id}', response_model=ShowUsers)
def get_user(user_id:int,session:Session = Depends(create_session),get_current_user: User =Depends(get_current_user)):
    user=session.query(User).filter(User.id==user_id).first()
    if not user:
        raise HTTPException(status_code=404,detail="User does not exist")
    return user

@router.post('/users')
def create_user(user:UsersCreate,session:Session=Depends(create_session)):
    if (session.query(User).filter(User.email==user.email).first()):
        raise HTTPException(status_code=400,detail="User already exists")
    hashed_password=password_hash.hash(user.password)
    new_user=User(
        name=user.name,
        age=user.age,
        email=user.email,
        password=hashed_password
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return {"message: user created"}
