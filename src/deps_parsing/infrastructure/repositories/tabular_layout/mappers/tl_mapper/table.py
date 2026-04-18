from typing import Any

from deps_tabular_layout.models import EntityId, Point, Table

from deps_parsing.domain.dtos import TableProjection, TableSchemaProjection

from ..cell_mapper import CellMapper
from .placement import PlacementMapper

__all__ = ["TableMapper"]


class TableMapper:
    @staticmethod
    def to_dict(tl_id: str, table: Table) -> dict[str, Any]:
        return {
            "id": table.id(),
            "tabular_layout_id": tl_id,
            "sheet_id": table.sheet_id(),
            "row_count": table.row_count,
            "column_count": table.column_count,
            "placement": PlacementMapper.to_dict(table.placement),
        }

    @staticmethod
    def table_from_dict(raw_data: dict[str, Any]) -> Table:
        return Table(
            id_=EntityId(raw_data["table_id"]),
            sheet_id=EntityId(raw_data["sheet_id"]),
            column_count=raw_data["column_count"],
            row_count=raw_data["row_count"],
            placement=(PlacementMapper.from_raw(raw_data["placement"])),
        )

    @staticmethod
    def table_projection_from_dict(raw_data: dict[str, Any]) -> TableProjection:
        return TableProjection(
            schema=TableSchemaProjection(
                id=raw_data["table_id"],
                sheet_id=raw_data["sheet_id"],
                column_count=raw_data["column_count"],
                row_count=raw_data["row_count"],
                placement=(Point(**raw_data["placement"][0]), Point(**raw_data["placement"][1])),
            ),
            data=[CellMapper.from_raw(cell) for cell in raw_data["cells"] if raw_data["cells"][0]["id"] is not None],
        )
