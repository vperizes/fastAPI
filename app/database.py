from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from .config import settings

load_dotenv()

# create DB URL/connection string
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.db_username}:{settings.db_password}@{settings.db_hostname}:{settings.db_port}/{settings.db_name}"

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
