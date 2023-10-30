from fastapi import FastAPI,status,HTTPException,Response,Depends
from fastapi.params import Body
from typing import Optional,List
from sqlalchemy.orm import Session
from passlib.context import CryptContext
import psycopg2
from psycopg2.extras import RealDictCursor #for returning column names after queries
import random
from . import models,schemas,utils
from .database import engine,get_db
from .routers import users,posts,auth

models. Base.metadata.create_all(bind=engine)

app = FastAPI()


#used when sql is used and not orm            
# try:
#     conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres',
#     password='Shubham@8223', cursor_factory=RealDictCursor)
#     cursor = conn.cursor()
#     print("Database connection was succesfull!")
# except Exception as error:
#     print("Connecting to database failed")
#     print("Error: ", error)


app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}


