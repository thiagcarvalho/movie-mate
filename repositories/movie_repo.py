from sqlalchemy.orm import Session
from utils.db_session import db_session
from models.movie import Movie

def get_movies() -> list[Movie]:
    with db_session() as db:
        return db.query(Movie).filter(Movie.viewed == False).all()

def get_movie_by_name(name: str) -> Movie:
    with db_session() as db:
        return db.query(Movie).filter(Movie.name == name).first()

def create_movie(name: str, duration: str, provider: str,
                 rating: float, poster_url: str, added_by: str) -> Movie:
    
    with db_session() as db:

        new_movie = Movie(name=name, duration=duration, provider=provider,
                        rating=rating, poster_url=poster_url, added_by=added_by)
        db.add(new_movie)
        db.commit()
        db.refresh(new_movie)

        return new_movie

def get_movies_names() -> list[str]:
    with db_session() as db:
        return [movie.name for movie in db.query(Movie).all()]

def update_movie(movie: Movie, **kwargs) -> bool:
    with db_session() as db:
        for key, value in kwargs.items():
            db.query(Movie).filter(Movie.id == movie.id).update({key: value})
        db.commit()
        
        return True

def delete_movie(movie: Movie) ->None:
    with db_session() as db:
        db.delete(movie)
        db.commit()