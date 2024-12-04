from fastapi import (
    FastAPI, Body, Query, Path, Request, HTTPException, Depends, APIRouter
)
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.encoders import jsonable_encoder

from models.schemas import Movie
from models.orm import MovieORM

from db.database import SessionLocal, get_db
from utils.jwt_handler import BearerJWT

from services.movies_services import *

router = APIRouter(tags=['Movies'])

#@router.get(path= '/movies', tags=['Movies'], dependencies=[Depends(BearerJWT())])
@router.get(path= '/movies', tags=['Movies'])
def get_movies(db: SessionLocal = Depends(get_db)):
    movies = get_all_movies_service(db)
    if movies:
        return JSONResponse(
            status_code=200,
            content=jsonable_encoder(movies))
    return JSONResponse(
        status_code=404,
        content={'Message': 'Not Movies Found'}
    )

#@router.post(path='/movies', tags=['Movies'], dependencies=[Depends(BearerJWT())])
@router.post(path='/movies', tags=['Movies'])
def create_movie(movie: Movie, db: SessionLocal = Depends(get_db)):
    new_movie: MovieORM = create_movie_service(db, movie)
    if new_movie:
        return JSONResponse(status_code=201, content={
            'Message': 'Movie created',
            'movie': movie.model_dump()
        })
    return JSONResponse(
        status_code=404,
        content={'Message': 'Not Movie Found'}
    )
@router.get(path='/movies/{id}', tags=['Movies'])
def get_movie(db: SessionLocal = Depends(get_db), id: int = Path(ge=1, title='Movie Id')):
    movie: MovieORM = get_movie_service(db, id)
    if movie:
        return JSONResponse(status_code=200, content={
            'message':  'Movie found',
            'movie': jsonable_encoder(movie)
        })
    return JSONResponse(status_code=404, content={
        'message': 'Movie not found',
    })

@router.get(path='/movies/', tags=['Movies'], status_code=200)
def get_movie_by_category(db: SessionLocal = Depends(get_db), category: str = Query(min_len=5, max_length=15)):
    movies = get_movie_by_category_service(db, category)
    if movies:
        return JSONResponse(
            status_code=200,
            content={'message': 'Category Found',
                     'movies': jsonable_encoder(movies)}
        )
    return JSONResponse(
        status_code=404,
        content={'message': 'Category not found'}
    )
@router.put(path='/movies/{id}', tags=['Movies'])
def update_movie(movie: Movie, db: SessionLocal = Depends(get_db), id:int = Path(ge=1, le=100)):
   update_movie = update_movie_service(db, id, movie)
   if update_movie:
        return JSONResponse(
            status_code=200,
            content={
                'message': 'Movie updated',
                'movie': jsonable_encoder(update_movie)
            }
        )
   return JSONResponse(
       status_code=404,
       content={'message': 'Movie not found'})

@router.delete(path='/movies/{id}', tags=['Movies'], status_code=200)
def delete_movie(id: int = Path(ge=1, le=100, title='Movie Id'), db: SessionLocal = Depends(get_db)):
    deleted_movie = delete_movie_service(db, id)
    if deleted_movie:
        return JSONResponse(status_code=200, content={
            'message': 'Movie deleted',
            'movie': jsonable_encoder(deleted_movie)
        })
    return JSONResponse(status_code=404, content={
        'message': 'Movie not found',
    })