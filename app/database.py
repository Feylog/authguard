from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import Config

SQLALCHEMY_DATABASE_URL = Config.DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency для использования в маршрутах
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()