from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse

app = FastAPI(
    title='Aprendiendo FastApi',
    description='Un API en los primeros pasos',
    version='0.0.1',
)

movies = [
    {
        'id': 1,
        'title': 'The Great Father',
        'overview': 'El Padrino es una pelicula de 1972 dirigida por Francis Ford Copola... ',
        'year': 1999,
        'raitin': 9.2,
        'category': 'Crimen'
    }
]

@app.get(path= '/', tags=['Inicio'])
def read_root():
    return HTMLResponse('<h1>Hello Movies</h1>')

@app.get(path= '/movies', tags=['Movies'])
def get_movies():
    return movies

@app.post(path='/movies', tags=['Movies'])
def create_movie(
        id: int = Body(),
        title: str = Body(),
        overview: str = Body(),
        year: int = Body(),
        raitin: float = Body(),
        category: str = Body()
):
    movies.append(
        {
            'id': id,
            'title': title,
            'overview': overview,
            'year': year,
            'raitin': raitin,
            'category': category
        }
    )
    return id

#Update a Movie
@app.put(path='/movies/{id}', tags=['Movies'])
def update_movie(
        id: int,
        title: str = Body(),
        overview: str = Body(),
        year: int = Body(),
        raitin: float = Body(),
        category: str = Body()
):
    item = next((item for item in movies if item['id'] == id), None)
    if item:
        item['title'] = title
        item['overview'] = overview
        item['year'] = year
        item['raitin'] = raitin
        item['category'] = category
    return item

#Delete a Movie
@app.delete(path='/movies/{id}', tags=['Movies'])
def delete_movie(id: int):
    item = next((item for item in movies if item['id'] == id), None)
    if item:
        movies.remove(item)
        return HTMLResponse(f'<p>Movie con id: {id} ha sido eliminada.</p>')
    return movies
