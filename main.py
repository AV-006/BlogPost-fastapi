from fastapi import FastAPI,Depends,HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from jwt.exceptions import InvalidTokenError
from pydantic import BaseModel
from sqlalchemy import create_engine, Column,Integer,String,Text,ForeignKey     
from sqlalchemy.orm import declarative_base,sessionmaker,Session,relationship 
from typing import List
from pwdlib import PasswordHash

SECRET_KEY = "fc0635a84612594ef01c4f0fb1406dac364a89b69d07ff8536f6906b0c4d5808"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

password_hash=PasswordHash.recommended()
DUMMY_HASH = password_hash.hash("dummypassword")

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
    author=relationship("User", back_populates="blogs")


class User(Base):
    __tablename__="users"
    id=Column(Integer, primary_key=True, index=True)
    name=Column(String, nullable=False)
    age=Column(Integer, nullable=False)
    email=Column(String, nullable=False)
    password=Column(String, nullable=False)
    blogs=relationship("Blogs",back_populates="author")

#create the tables
Base.metadata.create_all(bind=engine)


#request body

class BlogCreate(BaseModel):
    title: str
    content: str

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
    content: str
    # author: ShowUsers
    class Config:
        orm_mode=True


app=FastAPI()


#user routes
@app.get('/')
def home_route():
    return {"message": "home"}

@app.get('/users/{user_id}', response_model=ShowUsers,tags=["users"])
def get_user(user_id:int,session:Session = Depends(create_session)):
    user=session.query(User).filter(User.id==user_id).first()
    if not user:
        raise HTTPException(status_code=404,detail="User does not exist")
    return user

@app.post('/users',tags=["users"])
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


#blog routes
@app.post('/blogs/{user_id}',tags=["blogs"])
def create_blog(blog: BlogCreate, user_id:int, session: Session=Depends(create_session)):
    new_blog=Blogs(
        title=blog.title,
        content=blog.content,
        user_id=user_id
    )
    session.add(new_blog)
    session.commit()
    session.refresh(new_blog)
    return {"message":"blog created"}


@app.get('/blogs',response_model=List[ShowUsers],tags=["blogs"])
def get_all_blogs(session: Session=Depends(create_session)):
    blogs=session.query(User).all()
    return blogs


@app.get('/blogs/{user_id}',response_model=List[ShowUsers],tags=["blogs"])
def get_user_blogs(user_id: int,session:Session=Depends(create_session)):
    blogs=session.query(User).filter(User.id==user_id).all()
    return blogs

@app.delete('/blogs/{blog_id}',tags=["blogs"])
def delete_blog(blog_id: int, session: Session=Depends(create_session)):
    blog=session.query(Blogs).filter(Blogs.id==blog_id).first()
    if not blog:
        raise HTTPException(status_code=404,detail="blog not found")
    session.delete(blog)
    session.commit()
    return {"message": "blog deleted"}

@app.put('/blogs/{blog_id}',tags=["blogs"])
def update_blog(blog:BlogCreate,blog_id: int, session:Session=Depends(create_session)):
    current_blog=session.query(Blogs).filter(Blogs.id==blog_id).first()
    for key,value in blog.dict().items():
        setattr(current_blog,key,value)
    
    session.commit()
    session.refresh(current_blog)
    return {"message": "blog updated"}