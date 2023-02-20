# ./src/app/main.py

import logging
import logging.config
from uvicorn import run
from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from app.settings import get_settings

# from app.log_config import log_config

settings = get_settings()

# logging.config.dictConfig(log_config)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=".*",
    allow_credentials=True,
    allow_methods="*",
    allow_headers="*",
)


if __name__ == "__main__":
    run("main:app", host=settings.API_HOST, port=settings.API_PORT, reload=True)
