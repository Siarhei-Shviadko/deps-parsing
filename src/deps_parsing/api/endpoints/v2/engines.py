from fastapi import APIRouter, Query

from deps_parsing.api import MarkerRoute, Visibility
from deps_parsing.application import ENGINES, LayoutType

from ...serializers import EngineSerializer, EnginesResponse

__all__ = ["engines_router"]

engines_router = APIRouter(tags=["Parsing", "Version 2"], route_class=MarkerRoute)


@engines_router.get(
    "/engines",
    response_model=EnginesResponse,
    openapi_extra={"visibility": Visibility.PUBLIC},
)
def get_engines(
    layout_type: LayoutType | None = Query(default=None, alias="layoutType"),
) -> EnginesResponse:
    engines = ENGINES if layout_type is None else [engine for engine in ENGINES if engine.layout_type == layout_type]

    return EnginesResponse(
        engines=[
            EngineSerializer(code=engine.code, name=engine.name, layout_type=engine.layout_type) for engine in engines
        ],
    )
