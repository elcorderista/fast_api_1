from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional

class Movie(BaseModel):
    title: str = Field(default='Titulo de la pelicula', min_length=5, max_length=60)
    overview: str = Field(default='Movie Description', min_length=5, max_length=100)
    year: int = Field(default=1981)
    rating: float = Field(ge=1, le=10)
    category: str = Field(default='Movie Category', min_length=5, max_length=30)

    class Config:
        from_attributes = True

class User(BaseModel):

    email: EmailStr = Field(min_length=5, max_length=30)
    password:str = Field(min_length=8, max_length=100)

    class Config:
        from_attributes = True
