from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from src.books.routes import book_router
from contextlib import asynccontextmanager
from src.db.main import init_db
from src.auth.routes import auth_router
from src.reviews.routes import review_router
from src.tags.routes import tags_router
from .errors import register_all_errors

@asynccontextmanager #convierte la función en un contexto async, ideal para manejar recursos de arranque y cierre
async def life_span(app: FastAPI):
    print("server is starting ...")   # antes de levantar el server
    await init_db()                   # acá corrés tu inicialización (ej: test DB, crear tablas, seeds)
    yield                             # el control pasa al server
    print("server has been stoped")   # se ejecuta al apagar el server

version = "v1"

app = FastAPI(
    title="Bookly",
    description="A REST API for a book review web service",
    version= version,
    # lifespan=life_span
)


register_all_errors(app)


app.include_router(book_router, prefix=f"/api/{version}/books", tags=['books'])
app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=['auth'])
app.include_router(review_router, prefix=f"/api/{version}/reviews", tags=['reviews'])
app.include_router(tags_router, prefix=f"/api/{version}/tags", tags=['tags'])