import os
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from settings.config import Settings

settings = Settings()

sqliteName = settings.database_name
base_dir = settings.base_dir
databaseURL = settings.databaseURL

engine = create_engine(databaseURL, echo=True)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()