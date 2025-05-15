import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv
load_dotenv()

SQLITE_DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(SQLITE_DATABASE_URL, echo=True)

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine)

def get_db():
    with SessionLocal() as db:
        yield db