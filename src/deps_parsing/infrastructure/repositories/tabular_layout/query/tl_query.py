from typing import Optional

from deps_tabular_layout.models import TabularLayout

from deps_parsing.domain.dtos import TabularLayoutInfo, TabularLayoutProjection
from deps_parsing.domain.dtos.tabular_layout_filter import TabularLayoutFilter
from deps_parsing.domain.interfaces import ITabularLayoutQueryRepository
from deps_parsing.extras.datasource import Database

from ..mappers import TabularLayoutInfoMapper, TabularLayoutMapper
from .query_factory import DocumentLayoutQueryFactory

__all__ = ["TabularLayoutQueryRepository"]


class TabularLayoutQueryRepository(ITabularLayoutQueryRepository):
    def __init__(self, database: Database) -> None:
        self._db = database
        self._query_factory = DocumentLayoutQueryFactory()

    def layout_of_id(self, layout_id: str, tenant_id: str) -> Optional[TabularLayout]:
        query = self._query_factory.select_tabular_layout(layout_id=layout_id, tenant_id=tenant_id)

        with self._db.connection() as conn:
            result = conn.execute(query).fetchone()

        return TabularLayoutMapper.tl_from_dict(result) if result else None

    def layout_projection_of_id(
        self,
        layout_id: str,
        tenant_id: str,
        filtering: TabularLayoutFilter,
    ) -> Optional[TabularLayoutProjection]:
        query = self._query_factory.select_tabular_layout_with_cells_by(
            layout_id=layout_id,
            tenant_id=tenant_id,
            filtering=filtering,
        )

        with self._db.connection() as conn:
            result = conn.execute(query).fetchone()

        return TabularLayoutMapper.tl_projection_from_dict(result) if result else None

    def layout_of_id_info(self, layout_id: str, tenant_id: str) -> Optional[TabularLayoutInfo]:
        query = self._query_factory.select_layout_info(layout_id=layout_id, tenant_id=tenant_id)
        with self._db.connection() as conn:
            result = conn.execute(query).fetchone()

        return TabularLayoutInfoMapper.from_dict(result) if result else None

    def is_layout_exists(self, layout_id: str, tenant_id: str) -> bool:
        query = self._query_factory.select_layout_id(layout_id, tenant_id)
        with self._db.connection() as conn:
            result = conn.execute(query).fetchone()
        return bool(result)
