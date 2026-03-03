
from fastapi import FastAPI
from .blog.database import engine,Base
from .blog.routers import authentication,blog,user


from dotenv import load_dotenv
load_dotenv()

app=FastAPI()

#create the tables
Base.metadata.create_all(bind=engine)

app.include_router(authentication.router)
app.include_router(blog.router)
app.include_router(user.router)
































