
from dotenv import load_dotenv
import sqlite3
import os

load_dotenv()
DB_PATH = os.getenv('DB_PATH')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS movies (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   tmdb_id INTEGER,
                   name TEXT NOT NULL,
                   duration TEXT,
                   provider TEXT,
                   rating REAL,
                   added_by TEXT,
                   poster_url TEXT,
                   viewed BOOLEAN DEFAULT FALSE
                   )
        ''')
    conn.commit()
    conn.close()

init_db()

def add_movie(movie_name: str, tmdb_id: int, duration: float, providers: str, rating: float, poster_url: str, added_by: str) -> None:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    query = """
    INSERT INTO movies (name, tmdb_id, duration, provider, rating, poster_url, added_by)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """
    cursor.execute(query, (movie_name, tmdb_id, duration, providers, rating, poster_url, added_by))

    conn.commit()
    conn.close()

def get_movies() -> list:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(''' SELECT name, duration, provider, rating FROM movies WHERE viewed == FALSE ''')
    movies = cursor.fetchall()
    conn.close()

    return movies

def get_movies_names() -> list:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(''' SELECT name FROM movies WHERE viewed == FALSE ''')
    movies = cursor.fetchall()
    conn.close()

    return movies

def get_movie_info(movie_name: str) -> list:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(''' SELECT duration, provider, poster_url, id FROM movies  WHERE name = ? AND viewed == FALSE''', (movie_name,))
    movies = cursor.fetchall()
    conn.close()

    return movies

def get_movieid_by_name(movie_name: str) -> int:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(''' SELECT id FROM movies WHERE name = ? AND viewed == FALSE''', (movie_name,))
    movie_id = cursor.fetchone()
    conn.close()

    if not movie_id:
        return None
    
    return movie_id[0]

def update_movie(movied_id: int) -> bool:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(''' UPDATE movies SET viewed = TRUE WHERE id = ?''', (movied_id,))
    conn.commit()

    rows_affected = cursor.rowcount
    conn.close()

    if rows_affected == 0:
        return False
    
    return True

def delete_movie(movie_id: int) -> bool:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(''' DELETE FROM movies WHERE id = ? AND viewed == 0''', (movie_id,))
    conn.commit()

    rows_affected = cursor.rowcount
    conn.close()

    if rows_affected == 0:
        return False

    return True
    
