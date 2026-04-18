from http import HTTPStatus

from dependency_injector.wiring import Provide, inject
from deps_document_layout.model import DocumentLayoutFeaturesFilter, ParsingType
from deps_document_layout.serializers.document_layout import SerializedDocumentLayout
from fastapi import APIRouter, Body, Depends, Path, Response

from deps_parsing.api import MarkerRoute, Visibility, get_current_user_tenant
from deps_parsing.application import DocumentLayoutService
from deps_parsing.containers import Containers

from ...serializers import (
    UpdateImageRequest,
    UpdateKeyValuePairRequest,
    UpdateParagraphRequest,
    UpdateTableRequest,
)
from ..common_dependencies import DocumentLayoutFeaturesFilterFactory as FilterFactory

__all__ = ["document_layout_router"]

document_layout_router = APIRouter(
    prefix="/document-layout",
    tags=["Document Layout", "Version 2"],
    route_class=MarkerRoute,
)


@document_layout_router.get(
    "/{documentLayoutId}",
    status_code=HTTPStatus.OK,
    response_model=SerializedDocumentLayout,
    openapi_extra={"visibility": Visibility.PUBLIC},
)
@inject
def get_document_layout(
    document_layout_id: str = Path(..., alias="documentLayoutId"),
    current_tenant: str = Depends(get_current_user_tenant),
    filtering: DocumentLayoutFeaturesFilter = Depends(FilterFactory.make_filter),
    application: DocumentLayoutService = Depends(Provide[Containers.applications.document_layout_service]),
) -> SerializedDocumentLayout:
    document_layout = application.find_document_layout(
        document_layout_id=document_layout_id,
        tenant_id=current_tenant,
        filtering=filtering,
    )

    return SerializedDocumentLayout.from_model(document_layout)


@document_layout_router.patch(
    "/{documentLayoutId}/pages/{pageId}/paragraphs/{paragraphId}",
    status_code=HTTPStatus.OK,
    response_class=Response,
    openapi_extra={"visibility": Visibility.PUBLIC},
)
@inject
def update_paragraph(
    update_paragraph_request: UpdateParagraphRequest,
    layout_id: str = Path(..., alias="documentLayoutId"),
    page_id: str = Path(..., alias="pageId"),
    paragraph_id: str = Path(..., alias="paragraphId"),
    current_tenant: str = Depends(get_current_user_tenant),
    application: DocumentLayoutService = Depends(Provide[Containers.applications.document_layout_service]),
) -> None:
    application.update_paragraph(
        layout_id=layout_id,
        tenant_id=current_tenant,
        page_id=page_id,
        paragraph_id=paragraph_id,
        update_data=update_paragraph_request.update_data,
    )


@document_layout_router.put(
    "/{documentLayoutId}/user-parsing-type",
    response_class=Response,
    openapi_extra={"visibility": Visibility.PUBLIC},
    status_code=HTTPStatus.CREATED,
)
@inject
def clone_document_layout(
    document_layout_id: str = Path(..., alias="documentLayoutId"),
    parsing_type: str = Body(..., alias="parsingType", embed=True),
    current_tenant: str = Depends(get_current_user_tenant),
    application: DocumentLayoutService = Depends(Provide[Containers.applications.document_layout_service]),
) -> None:
    application.clone_pages(
        document_layout_id=document_layout_id,
        tenant_id=current_tenant,
        original_parsing_type=ParsingType(parsing_type),
    )


@document_layout_router.patch(
    "/{documentLayoutId}/pages/{pageId}/images/{imageId}",
    status_code=HTTPStatus.OK,
    openapi_extra={"visibility": Visibility.PUBLIC},
)
@inject
def update_document_layout_image(
    data: UpdateImageRequest,
    document_layout_id: str = Path(..., alias="documentLayoutId"),
    page_id: str = Path(..., alias="pageId"),
    image_id: str = Path(..., alias="imageId"),
    current_tenant: str = Depends(get_current_user_tenant),
    application: DocumentLayoutService = Depends(Provide[Containers.applications.document_layout_service]),
) -> None:
    application.update_image(
        layout_id=document_layout_id,
        page_id=page_id,
        image_id=image_id,
        tenant_id=current_tenant,
        title=data.title,
        description=data.description,
        polygon=data.polygon,
        filepath=data.filepath,
    )


@document_layout_router.patch(
    "/{documentLayoutId}/pages/{pageId}/tables/{tableId}",
    status_code=HTTPStatus.OK,
    response_class=Response,
    openapi_extra={"visibility": Visibility.PUBLIC},
)
@inject
def update_table(
    update_table_request: UpdateTableRequest,
    layout_id: str = Path(..., alias="documentLayoutId"),
    page_id: str = Path(..., alias="pageId"),
    table_id: str = Path(..., alias="tableId"),
    current_tenant: str = Depends(get_current_user_tenant),
    application: DocumentLayoutService = Depends(Provide[Containers.applications.document_layout_service]),
) -> None:
    application.update_table(
        layout_id=layout_id,
        tenant_id=current_tenant,
        page_id=page_id,
        table_id=table_id,
        update_data=update_table_request.update_data,
    )


@document_layout_router.patch(
    "/{documentLayoutId}/pages/{pageId}/key-value-pairs/{keyValuePairId}",
    status_code=HTTPStatus.OK,
    response_class=Response,
    openapi_extra={"visibility": Visibility.PUBLIC},
)
@inject
def update_key_value_pair(
    update_key_value_pair_request: UpdateKeyValuePairRequest,
    layout_id: str = Path(..., alias="documentLayoutId"),
    page_id: str = Path(..., alias="pageId"),
    key_value_pair_id: str = Path(..., alias="keyValuePairId"),
    current_tenant: str = Depends(get_current_user_tenant),
    application: DocumentLayoutService = Depends(Provide[Containers.applications.document_layout_service]),
) -> None:
    application.update_key_value_pair(
        layout_id=layout_id,
        tenant_id=current_tenant,
        page_id=page_id,
        key_value_pair_id=key_value_pair_id,
        update_data=update_key_value_pair_request.update_data,
    )
