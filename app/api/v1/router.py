from fastapi import APIRouter
from app.api.v1.endpoints import bullet

api_router = APIRouter()

# Include bullet endpoints
api_router.include_router(bullet.router, tags=["bullet"]) 