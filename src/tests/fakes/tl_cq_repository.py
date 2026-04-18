from typing import Any, Optional

from deps_tabular_layout.models import TabularLayout

from deps_parsing.domain.dtos import TabularLayoutInfo
from deps_parsing.domain.interfaces import (
    ITabularLayoutCommandRepository,
    ITabularLayoutQueryRepository,
)
from deps_parsing.infrastructure.repositories.tabular_layout import (
    TabularLayoutInfoMapper,
)

__all__ = ["FakeTabularLayoutCommandQueryRepository"]


class FakeTabularLayoutCommandQueryRepository(
    ITabularLayoutCommandRepository,
    ITabularLayoutQueryRepository,
):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_singleton_instance"):
            setattr(cls, "_singleton_instance", super(FakeTabularLayoutCommandQueryRepository, cls).__new__(cls))

        return getattr(cls, "_singleton_instance")

    def __init__(self) -> None:
        if not hasattr(self, "_db"):
            self._db: dict[tuple[str, str], TabularLayout] = {}

    def __enter__(self) -> "FakeTabularLayoutCommandQueryRepository":
        return self

    def __exit__(self, *args: Any, **kwargs: Any) -> None:
        self._db.clear()

    def save(self, layout: TabularLayout) -> None:
        self._db[layout.id(), layout.tenant_id()] = layout

    def local_db(self) -> dict[tuple[str, str], TabularLayout]:
        return self._db

    def delete(self, layout_id: str, tenant_id: str) -> None:
        del self._db[(layout_id, tenant_id)]

    def layout_of_id(self, layout_id: str, tenant_id: str) -> Optional[TabularLayout]:
        return self._db.get((layout_id, tenant_id))

    def is_layout_exists(self, layout_id: str, tenant_id: str) -> bool:
        return bool(self._db.get((layout_id, tenant_id)))

    def layout_of_id_info(self, layout_id: str, tenant_id: str) -> Optional[TabularLayoutInfo]:
        if tl := self._db.get((layout_id, tenant_id)):
            return TabularLayoutInfoMapper.from_dict(
                {
                    "tabular_layout_id": tl.id(),
                    "parsing_type": tl.parsing_type,
                    "sheets": [
                        {
                            "id": sheet.id(),
                            "title": sheet.title,
                            "is_hidden": sheet.is_hidden,
                            "images": [{"id": image.id()} for image in sheet.images],
                        }
                        for sheet in tl.sheets
                    ],
                    "tables_info": [
                        {
                            "table_id": table.id(),
                            "sheet_id": table.sheet_id(),
                            "row_count": table.row_count,
                            "column_count": table.column_count,
                            "placement": [
                                {"x": table.placement[0].x, "y": table.placement[0].y},
                                {"x": table.placement[1].x, "y": table.placement[1].y},
                            ],
                        }
                        for sheet in tl.sheets
                        for table in sheet.tables
                    ],
                },
            )
