from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine, Column,Integer,String,Text     
from sqlalchemy.orm import declarative_base 

url="postgresql://postgres:password@localhost:5432/fastapi_db"

engine=create_engine(url,echo=True)
Base=declarative_base()
class User(Base):
    __tablename__="users"
    id=Column(Integer, primary_key=True, index=True)
    name=Column(String, nullable=False)
    age=Column(Integer, nullable=False)
    email=Column(String, nullable=False)

class Blogs(Base):
    __tablename__="blogs"
    id=Column(Integer, primary_key=True, index=True)
    content=Column(Text, nullable=False)



app=FastAPI()

