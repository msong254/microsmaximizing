from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://microsmaximizing_db_user:3HcvTPa8IBsEyBJVzycJ3O7m78PsBWJ4@dpg-d2ie60emcj7s738df770-a.oregon-postgres.render.com/microsmaximizing_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()