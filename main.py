from typing import List

from fastapi import Depends, FastAPI, HTTPException

import database
import schemas
import models
from database import db_state_default

app = FastAPI()

@app.get("/movies/", response_model=List[schemas.Movie])
def get_movies():
    return list(models.Movie.select())
    # movies = crud.get_movies()
    # return movies

@app.post("/movies/", response_model=schemas.Movie)
def add_movie(movie: schemas.MovieBase):
    movie = models.Movie.create(**movie.dict())
    return movie

@app.get("/movies/{movie_id}", response_model=schemas.Movie)
def get_movie(movie_id: int):
    db_movie = models.Movie.filter(models.Movie.id == movie_id).first()
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return db_movie

@app.delete("/movies/{movie_id}", response_model=schemas.Movie)
def delete_movie(movie_id: int):
    db_movie = models.Movie.filter(models.Movie.id == movie_id).first()
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    db_movie.delete_instance()
    return db_movie

#zadania --------------------------------

#pobieranie wszystkich aktorów w bazie danych
@app.get("/actors/", response_model=List[schemas.Actor])
def get_actors():
    db_actors= models.Actor.select()
    if db_actors is None:
        raise HTTPException(status_code=404, detail="Actors not found")
    return list(db_actors)

#pobieranie pojedynczego aktora
@app.get("/actors/{actor_id}", response_model=schemas.Actor)
def get_movie(actor_id: int):
    db_actors = models.Actor.filter(models.Actor.id == actor_id).first()
    if db_actors is None:
        raise HTTPException(status_code=404, detail="Actor not found")
    return db_actors

#dodawanie aktora do bazy
@app.post("/actors/", response_model=schemas.Actor)
def add_actor(actor: schemas.ActorBase):
    actor = models.Actor.create(**actor.dict())
    return actor

#usuwanie aktora
@app.delete("/actors/{actor_id}", response_model=schemas.Actor)
def delete_actor(actor_id: int):
    db_actor = models.Actor.filter(models.Actor.id == actor_id).first()
    if db_actor is None:
        raise HTTPException(status_code=404, detail="Actor not found")
    db_actor.delete_instance()
    return db_actor

#usuwanie aktora
@app.post("/movies/{movie_id}/actors", response_model=schemas.Movie)
def add_actor_to_movie(movie_id: int, actor_id: int):
    
    ## pobrane movie
    db_movie = models.Movie.filter(models.Movie.id == movie_id).first()
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    #pobierz aktora
    db_actors = models.Actor.filter(models.Actor.id == actor_id).first()
    if db_actors is None:
        raise HTTPException(status_code=404, detail="Actor not found")
    
    #sprawdzanie czy aktor już tam nie jest
    if db_actors in db_movie.actors:
        raise HTTPException(status_code=400, detail="Actor is already assigned to this movie")
    
    db_movie.actors.add(db_actors)
    
    return db_movie
