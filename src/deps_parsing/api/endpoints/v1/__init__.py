from fastapi import APIRouter

from .document_layout import document_layout_router

__all__ = ["v1_router"]

v1_router = APIRouter()

v1_router.include_router(document_layout_router)
