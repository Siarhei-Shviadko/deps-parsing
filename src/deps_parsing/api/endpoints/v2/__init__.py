from fastapi import APIRouter

from .document_layout import *
from .engines import *
from .layout_info import *
from .tabular_layout import *

__all__ = ["v2_router"]

v2_router = APIRouter()
v2_router.include_router(layout_router)
v2_router.include_router(document_layout_router)
v2_router.include_router(tabular_layout_router)
v2_router.include_router(engines_router)
