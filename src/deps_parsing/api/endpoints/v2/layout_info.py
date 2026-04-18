from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Path

from deps_parsing.api import MarkerRoute, Visibility, get_current_user_tenant
from deps_parsing.application import ParsingService
from deps_parsing.containers import Containers

from ...serializers import SerializedParsingInfo

__all__ = ["layout_router"]

layout_router = APIRouter(prefix="/documents", tags=["Parsing"], route_class=MarkerRoute)


@layout_router.get(
    "/{documentId}/parsing-info",
    response_model=SerializedParsingInfo,
    openapi_extra={"visibility": Visibility.PUBLIC},
)
@inject
def get_parsing_info(
    document_id: str = Path(..., alias="documentId"),
    tenant_id: str = Depends(get_current_user_tenant),
    application: ParsingService = Depends(Provide[Containers.applications.parsing_service]),
):
    return SerializedParsingInfo.from_model(
        application.get_parsing_info(document_id, tenant_id),
    )
