from sqlalchemy.orm import Session
from contextlib import contextmanager
from database import engine

@contextmanager
def db_session():
    db = Session(bind=engine)
    try:
        yield db
    finally:
        db.close()