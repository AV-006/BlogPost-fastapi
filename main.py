from fastapi import FastAPI,Depends,HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column,Integer,String,Text,ForeignKey     
from sqlalchemy.orm import declarative_base,sessionmaker,Session,relationship 
from typing import List

url="postgresql://postgres:password@localhost:5432/fastapi_db"

engine=create_engine(url,echo=True)

#now create a session

sessionLocal=sessionmaker(bind=engine)

#dependency for session

def create_session():
    db=sessionLocal()
    try:
        yield db
    finally:
        db.close()



Base=declarative_base()

class Blogs(Base):
    __tablename__="blogs"
    id=Column(Integer, primary_key=True, index=True)
    title=Column(String, nullable=False)
    content=Column(Text, nullable=False)
    user_id=Column(Integer, ForeignKey("users.id") )
    blog=relationship("User", back_populates="creator")


class User(Base):
    __tablename__="users"
    id=Column(Integer, primary_key=True, index=True)
    name=Column(String, nullable=False)
    age=Column(Integer, nullable=False)
    email=Column(String, nullable=False)
    creator=relationship("Blogs",back_populates="blog")

#create the tables
Base.metadata.create_all(bind=engine)


#request body

class BlogCreate(BaseModel):
    title: str
    body: str

class UsersCreate(BaseModel):
    name: str
    age: int
    email: str
    password: str

#response body
class ShowUsers(BaseModel):
    id: int
    name: str
    age: int
    blogs: List[BlogCreate]=[]
    class Config:
        orm_mode=True



class ShowBlogs(BaseModel):
    id: int
    title: str
    body: str
    author: ShowUsers
    class Config:
        orm_mode=True


app=FastAPI()



@app.get('/')
def home_route():
    return {"message": "home"}

@app.get('/users/{user_id}', response_model=ShowUsers)
def get_user(user_id:int,session:Session = Depends(create_session)):
    user=session.query(User).filter(User.id==user_id).first()
    if not user:
        raise HTTPException(status_code=404,detail="User does not exist")
    return user

@app.post('/users')
def create_user(user:UsersCreate,session:Session=Depends(create_session)):
    if (session.query(User).filter(User.email==user.email).first()):
        raise HTTPException(status_code=400,detail="User already exists")
    new_user=User(
        name=user.name,
        age=user.age,
        email=user.email
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return {"message: user created"}