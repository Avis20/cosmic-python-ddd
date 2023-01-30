import logging
import logging.config
from uvicorn import run
from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from app.settings import get_settings
from app.log_config import log_config
from app.routers.base import base_router

from app.models.db import metadata, engine
import app.models.base

settings = get_settings()

logging.config.dictConfig(log_config)

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
    metadata.create_all(engine)


if __name__ == "__main__":
    run("main:app", host=settings.API_HOST, port=settings.API_PORT, reload=True)
