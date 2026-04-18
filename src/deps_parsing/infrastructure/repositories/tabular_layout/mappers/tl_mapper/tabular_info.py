from collections import defaultdict
from typing import Any

from deps_tabular_layout.models import ParsingType

from deps_parsing.domain.dtos import SheetInfo, TableInfo, TabularLayoutInfo

__all__ = ["TabularLayoutInfoMapper"]


class TabularLayoutInfoMapper:
    @staticmethod
    def from_dict(raw_data: dict[str, Any]) -> TabularLayoutInfo:
        tables_info = defaultdict(list)

        sheet_order = {sheet["id"]: idx for idx, sheet in enumerate(raw_data["sheets"])}
        tables_sorted = sorted(
            raw_data["tables_info"],
            key=lambda t: (
                sheet_order.get(t["sheet_id"], float("inf")),
                t["placement"][0]["y"] if t["placement"] else float("inf"),
                t["placement"][0]["x"] if t["placement"] else float("inf"),
            ),
        )

        for raw_table in tables_sorted if "tables_info" in raw_data else []:
            tables_info[raw_table["sheet_id"]].append(TableInfoMapper.from_dict(raw_table))

        return TabularLayoutInfo(
            id=raw_data["tabular_layout_id"],
            parsing_type=ParsingType(raw_data["parsing_type"]),
            sheets=[SheetInfoMapper.from_dict(sheet, tables_info.get(sheet["id"], [])) for sheet in raw_data["sheets"]],
        )


class SheetInfoMapper:
    @staticmethod
    def from_dict(raw_data: dict[str, Any], tables_info: list[TableInfo]) -> SheetInfo:
        return SheetInfo(
            id=raw_data["id"],
            title=raw_data["title"],
            is_hidden=raw_data["is_hidden"],
            tables=tables_info,
            images=[image["id"] for image in raw_data["images"]],
        )


class TableInfoMapper:
    @staticmethod
    def from_dict(raw_data: dict[str, Any]) -> TableInfo:
        return TableInfo(
            id=raw_data["table_id"],
            row_count=raw_data["row_count"],
            column_count=raw_data["column_count"],
        )
