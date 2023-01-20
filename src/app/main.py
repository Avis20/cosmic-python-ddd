from uvicorn import run
from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from app.settings import get_settings
from app.routers.base import base_router

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

if __name__ == "__main__":
    run("main:app", host=settings.API_HOST, port=settings.API_PORT, reload=True)
