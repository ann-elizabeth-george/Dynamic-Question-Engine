from fastapi import APIRouter
from app.api.v1 import auth, categories, questions, assessment

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(categories.router, prefix="/categories", tags=["categories"])
api_router.include_router(questions.router, prefix="/questions", tags=["questions"])
api_router.include_router(assessment.router, prefix="/assessment", tags=["assessment"])
