from db.database import SessionLocal
from models.orm import MovieORM
from models.schemas import Movie

def get_all_movies_service(db: SessionLocal):

    movies = db.query(MovieORM).all()
    return movies

def get_movie_service(db: SessionLocal, movie_id):
    movie: MovieORM = db.query(MovieORM).filter_by(id=movie_id).first()
    return movie

def get_movie_by_category_service(db: SessionLocal, movie_category):
    movies = db.query(MovieORM).filter_by(category=movie_category).all()
    return movies

def create_movie_service(db: SessionLocal, movie: Movie):
    newMovie: MovieORM = MovieORM(**movie.model_dump())
    db.add(newMovie)
    db.commit()
    db.refresh(newMovie)
    return newMovie

def update_movie_service(db: SessionLocal, movie_id: int, movie: Movie):
    updated_movie: MovieORM = db.query(MovieORM).filter_by(id=movie_id).first()
    if updated_movie:
        updated_movie.title = movie.title
        updated_movie.overview = movie.overview
        updated_movie.year = movie.year
        updated_movie.category = movie.category
        updated_movie.rating = movie.rating
        db.commit()
        db.refresh(updated_movie)
        return updated_movie

def delete_movie_service(db: SessionLocal, movie_id):
    movie = db.query(MovieORM).filter_by(id=movie_id).first()
    if movie:
        db.delete(movie)
        db.commit()
        return movie
    return None


