from pydantic import BaseModel
from typing import List
#request body

class BlogCreate(BaseModel):
    title: str
    content: str

class UsersCreate(BaseModel):
    name: str
    age: int
    email: str
    password: str

class UsersLogin(BaseModel):
    email:str
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

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    email: str | None=None