from typing import Any

from deps_tabular_layout.models import EntityId, Sheet

from deps_parsing.domain.dtos import SheetProjection

from .image import ImageMapper
from .table import TableMapper

__all__ = ["SheetMapper"]


class SheetMapper:
    @staticmethod
    def to_dict(sheet: Sheet) -> dict[str, Any]:
        return {
            "id": sheet.id(),
            "title": sheet.title,
            "is_hidden": sheet.is_hidden,
            "table_ids": [table.id() for table in sheet.tables],
            "images": [ImageMapper.to_dict(image) for image in sheet.images],
        }

    @staticmethod
    def sheet_from_dict(raw_sheet: dict[str, Any], raw_tables: list[dict[str, Any]]) -> Sheet:
        return Sheet(
            id_=EntityId(raw_sheet["id"]),
            title=raw_sheet["title"],
            is_hidden=raw_sheet["is_hidden"],
            tables=[TableMapper.table_from_dict(table) for table in raw_tables],
            images=[ImageMapper.from_dict(image) for image in raw_sheet["images"]],
        )

    @staticmethod
    def sheet_projection_from_dict(raw_data: dict[str, Any]) -> SheetProjection:
        return SheetProjection(
            id=raw_data["id"],
            title=raw_data["title"],
            images=[ImageMapper.from_dict(image) for image in raw_data["images"]],
            is_hidden=raw_data["is_hidden"],
            table_ids=raw_data["table_ids"],
        )
