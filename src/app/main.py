from uvicorn import run
from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from app.settings import get_settings
from app.models.base import start_mapper
from app.routers.base import base_router

from app.models.base import metadata
from app.models.db import engine 

settings = get_settings()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=".*",
    allow_credentials=True,
    allow_methods="*",
    allow_headers="*",
)
app.include_router(base_router)

@app.on_event("startup")
async def startup():
    start_mapper()
    metadata.create_all(engine)


if __name__ == "__main__":
    run("main:app", host=settings.API_HOST, port=settings.API_PORT, reload=True)
