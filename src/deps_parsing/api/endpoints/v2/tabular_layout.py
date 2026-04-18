import logging
from http import HTTPStatus

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Path

from deps_parsing.api import MarkerRoute, Visibility, get_current_user_tenant
from deps_parsing.application import TabularLayoutService
from deps_parsing.containers import Containers
from deps_parsing.domain.dtos import TabularLayoutFilter

from ...serializers.v2 import SerializedTabularLayout
from ..common_dependencies import TabularLayoutFeaturesFilterFactory as FilterFactory

__all__ = ["tabular_layout_router"]

_logger = logging.getLogger(__name__)

tabular_layout_router = APIRouter(
    prefix="/tabular-layout",
    tags=["Tabular Layout", "Version 2"],
    route_class=MarkerRoute,
)


@tabular_layout_router.get(
    "/{tabularLayoutId}",
    status_code=HTTPStatus.OK,
    response_model=SerializedTabularLayout,
    openapi_extra={"visibility": Visibility.PUBLIC},
)
@inject
def get_tabular_layout(
    tabular_layout_id: str = Path(..., alias="tabularLayoutId"),
    current_tenant: str = Depends(get_current_user_tenant),
    filtering: TabularLayoutFilter = Depends(FilterFactory.make_filter),
    application: TabularLayoutService = Depends(Provide[Containers.applications.tabular_layout_service]),
) -> SerializedTabularLayout:
    tl = application.find_tabular_layout(
        layout_id=tabular_layout_id,
        tenant_id=current_tenant,
        filtering=filtering,
    )

    return SerializedTabularLayout.from_model(tl)
