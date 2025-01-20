from sqlalchemy import Column, Integer, String, Boolean, Float
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from database import Base


class Movie(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    tmdb_id = Column(Integer, index=True)
    name = Column(String, index=True)
    duration = Column(String)
    provider= Column(String)
    rating = Column(Float)
    poster_url = Column(String)
    added_by = Column(String)
    viewed = Column(Boolean, default=False)
