from http import HTTPStatus

from dependency_injector.wiring import Provide, inject
from deps_document_layout.model import DocumentLayoutFeaturesFilter
from deps_document_layout.serializers.document_layout import (
    SerializedDocumentLayout,
    SerializedDocumentLayoutInfo,
    SerializedPage,
)
from fastapi import APIRouter, Depends, Path, Response

from deps_parsing.api.auth import get_current_user_tenant
from deps_parsing.api.endpoint_marker import MarkerRoute
from deps_parsing.api.endpoint_visibility import Visibility
from deps_parsing.api.serializers import (
    GetDocumentLayoutPagesResponse,
    SaveDocumentLayoutPagesRequest,
)
from deps_parsing.application import DocumentLayoutService
from deps_parsing.containers import Containers

from ..common_dependencies import DocumentLayoutFeaturesFilterFactory as FilterFactory

__all__ = ["document_layout_router"]

document_layout_router = APIRouter(prefix="/document-layout", tags=["Document Layout"], route_class=MarkerRoute)


@document_layout_router.post(
    "",
    openapi_extra={"visibility": Visibility.INTERNAL},
    response_class=Response,
    status_code=HTTPStatus.CREATED,
)
@inject
def create_document_layout(
    serialized_document_layout: SerializedDocumentLayout,
    current_tenant: str = Depends(get_current_user_tenant),
    application: DocumentLayoutService = Depends(Provide[Containers.applications.document_layout_service]),
) -> None:
    application.save_raw_document_layout(serialized_document_layout.to_dict(current_tenant))


@document_layout_router.get(
    "/{documentLayoutId}",
    response_model=SerializedDocumentLayout,
    openapi_extra={"visibility": Visibility.INTERNAL},
)
@inject
def get_document_layout(
    document_layout_id: str = Path(..., alias="documentLayoutId"),
    filtering: DocumentLayoutFeaturesFilter = Depends(FilterFactory.make_base_filter),
    current_tenant: str = Depends(get_current_user_tenant),
    application: DocumentLayoutService = Depends(Provide[Containers.applications.document_layout_service]),
) -> SerializedDocumentLayout:
    return SerializedDocumentLayout.from_model(
        application.get_or_create_document_layout(
            document_layout_id=document_layout_id,
            tenant_id=current_tenant,
            filtering=filtering,
        ),
    )


@document_layout_router.get(
    "/{documentLayoutId}/info",
    response_model=SerializedDocumentLayoutInfo,
    openapi_extra={"visibility": Visibility.INTERNAL},
)
@inject
def get_document_layout_info(
    document_layout_id: str = Path(..., alias="documentLayoutId"),
    current_tenant: str = Depends(get_current_user_tenant),
    application: DocumentLayoutService = Depends(Provide[Containers.applications.document_layout_service]),
):
    return SerializedDocumentLayoutInfo.from_model(
        application.get_or_create_document_layout_info(document_layout_id, current_tenant),
    )


@document_layout_router.put("/info", response_class=Response, openapi_extra={"visibility": Visibility.INTERNAL})
@inject
def save_document_layout_info(
    serialized_document_layout_info: SerializedDocumentLayoutInfo,
    current_tenant: str = Depends(get_current_user_tenant),
    application: DocumentLayoutService = Depends(Provide[Containers.applications.document_layout_service]),
) -> None:
    application.save_document_layout_info(serialized_document_layout_info.to_model(current_tenant))


@document_layout_router.get(
    "/{documentLayoutId}/pages",
    response_model=GetDocumentLayoutPagesResponse,
    openapi_extra={"visibility": Visibility.INTERNAL},
)
@inject
def get_document_layout_pages(
    document_layout_id: str = Path(..., alias="documentLayoutId"),
    filtering: DocumentLayoutFeaturesFilter = Depends(FilterFactory.make_filter_with_default_pagination),
    current_tenant: str = Depends(get_current_user_tenant),
    application: DocumentLayoutService = Depends(Provide[Containers.applications.document_layout_service]),
) -> GetDocumentLayoutPagesResponse:
    pages, total = application.get_document_layout_pages_with_page_amount(
        document_layout_id=document_layout_id,
        tenant_id=current_tenant,
        filtering=filtering,
    )

    return GetDocumentLayoutPagesResponse(
        total=total,
        pages=[SerializedPage.from_model(page) for page in pages],
    )


@document_layout_router.put(
    "/{documentLayoutId}/pages",
    response_class=Response,
    openapi_extra={"visibility": Visibility.INTERNAL},
)
@inject
def save_document_layout_pages(
    save_document_layout_pages_request: SaveDocumentLayoutPagesRequest,
    document_layout_id: str = Path(..., alias="documentLayoutId"),
    current_tenant: str = Depends(get_current_user_tenant),
    application: DocumentLayoutService = Depends(Provide[Containers.applications.document_layout_service]),
) -> None:
    application.save_document_layout_pages(
        document_layout_id=document_layout_id,
        tenant_id=current_tenant,
        pages=save_document_layout_pages_request.to_dict(document_layout_id),
    )
