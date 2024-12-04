from fastapi import (
    FastAPI, Body, Query, Path, Request, HTTPException, Depends
)
from fastapi.responses import HTMLResponse, JSONResponse
from routes import user
from routes import movies
from db.database import engine, Base

app = FastAPI(
    title='Aprendiendo FastApi',
    description='Un API en los primeros pasos',
    version='0.0.2',
)

# ==================================
# Define Routes
# ==================================
app.include_router(user.router)
app.include_router(movies.router)

# ==================================
# Generate DataBase
# ==================================
Base.metadata.create_all(bind=engine)

@app.get(path= '/', tags=['Inicio'])
def read_root():
    return HTMLResponse('<h1>Hello Movies</h1>')
