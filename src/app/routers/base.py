from fastapi import APIRouter
from app.routers import root

base_router = APIRouter()

base_router.include_router(root.router, tags=["root"])
