from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLACHEMY_DATABASE_URI = 'sqlite:///data.db'
engine = create_engine(SQLACHEMY_DATABASE_URI)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()