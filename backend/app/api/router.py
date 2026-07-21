from fastapi import APIRouter
from app.api.v1 import areas
from app.api.v1 import (
    auth,
    categories,
    questions,
    assessment,
    districts,
)

api_router = APIRouter()

api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["Authentication"],
)

api_router.include_router(
    categories.router,
    prefix="/categories",
    tags=["Categories"],
)
api_router.include_router(
    areas.router,
    prefix="/areas",
    tags=["Areas"]
)
api_router.include_router(
    questions.router,
    prefix="/questions",
    tags=["Questions"],
)

api_router.include_router(
    assessment.router,
    prefix="/assessment",
    tags=["Assessment"],
)

# NEW
api_router.include_router(
    districts.router,
    prefix="/districts",
    tags=["Districts"],
)