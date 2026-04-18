from typing import Any

from deps_tabular_layout.models import (
    CellProperties,
    EntityId,
    ParsingType,
    TabularLayout,
    TenantId,
)

from deps_parsing.domain.dtos import TabularLayoutProjection

from .sheet import SheetMapper
from .table import TableMapper

__all__ = ["TabularLayoutMapper"]


class TabularLayoutMapper:
    @staticmethod
    def tl_to_dict(tabular_layout: TabularLayout) -> dict[str, Any]:
        return {
            "id": tabular_layout.id(),
            "tenant_id": tabular_layout.tenant_id(),
            "parsing_type": tabular_layout.parsing_type,
            "sheets": [SheetMapper.to_dict(sheet) for sheet in tabular_layout.sheets],
            "extracted_properties": tabular_layout.extracted_properties,
        }

    @staticmethod
    def tl_to_raw_tables(tabular_layout: TabularLayout) -> list[dict[str, Any]]:
        return [TableMapper.to_dict(tl_id=tabular_layout.id(), table=table) for table in tabular_layout.iter_tables()]

    @staticmethod
    def tl_from_dict(raw_data: dict[str, Any]) -> TabularLayout:
        return TabularLayout(
            id_=EntityId(raw_data["tabular_layout_id"]),
            tenant_id=TenantId(raw_data["tenant_id"]),
            parsing_type=ParsingType(raw_data["parsing_type"]),
            extracted_properties=[CellProperties(prop) for prop in raw_data["extracted_properties"]],
            sheets=[
                SheetMapper.sheet_from_dict(
                    raw_sheet=sheet,
                    raw_tables=[table for table in raw_data["tables"] if table["sheet_id"] == sheet["id"]],
                )
                for sheet in raw_data["sheets"]
            ],
        )

    @staticmethod
    def tl_projection_from_dict(raw_data: dict[str, Any]) -> TabularLayoutProjection:
        sheet_order = {sheet["id"]: idx for idx, sheet in enumerate(raw_data["sheets"])}
        tables_sorted = sorted(
            raw_data["tables"],
            key=lambda t: (
                sheet_order.get(t["sheet_id"], float("inf")),
                t["placement"][0]["y"] if t["placement"] else float("inf"),
                t["placement"][0]["x"] if t["placement"] else float("inf"),
            ),
        )

        return TabularLayoutProjection(
            id=raw_data["tabular_layout_id"],
            tenant_id=raw_data["tenant_id"],
            parsing_type=ParsingType(raw_data["parsing_type"]),
            extracted_properties=[CellProperties(prop) for prop in raw_data["extracted_properties"]],
            sheets=[SheetMapper.sheet_projection_from_dict(sheet) for sheet in raw_data["sheets"]],
            tables=[
                TableMapper.table_projection_from_dict(table)
                for table in tables_sorted
                if raw_data["tables"][0]["table_id"] is not None
            ],
        )
