from sqlalchemy import create_engine
import os
from sqlalchemy.orm import sessionmaker,declarative_base
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine=create_engine(DATABASE_URL,echo=True)
Base=declarative_base()

#now create a session

sessionLocal=sessionmaker(bind=engine)

#dependency for session

def create_session():
    db=sessionLocal()
    try:
        yield db
    finally:
        db.close()

