from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# create DB URL/connection string
SQLALCHEMY_DATABASE_URL = f"postgresql://{os.getenv("USER")}:{os.getenv("PASS")}@{os.getenv("HOSTNAME")}/{os.getenv("DBNAME")}"

# create a SQLAlchemy "engine"
engine=create_engine(SQLALCHEMY_DATABASE_URL)

#create instance of sessionlocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# declartive_base() returns a class. we inherit from this class to create each of the db models or classes
Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
