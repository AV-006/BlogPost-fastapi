from sqlalchemy import Column,Integer,String,Text,ForeignKey
from sqlalchemy.orm import declarative_base,relationship     

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
