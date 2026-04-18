from abc import abstractmethod
from typing import Optional

from deps_tabular_layout.models import TabularLayout

from ...dtos import TabularLayoutFilter, TabularLayoutInfo, TabularLayoutProjection

__all__ = ["ITabularLayoutQueryRepository"]


class ITabularLayoutQueryRepository:
    @abstractmethod
    def layout_of_id(
        self,
        layout_id: str,
        tenant_id: str,
    ) -> Optional[TabularLayout]:
        ...

    @abstractmethod
    def layout_projection_of_id(
        self,
        layout_id: str,
        tenant_id: str,
        filtering: TabularLayoutFilter,
    ) -> Optional[TabularLayoutProjection]:
        ...

    @abstractmethod
    def is_layout_exists(self, layout_id: str, tenant_id: str) -> bool:
        ...

    @abstractmethod
    def layout_of_id_info(self, layout_id: str, tenant_id: str) -> Optional[TabularLayoutInfo]:
        ...
