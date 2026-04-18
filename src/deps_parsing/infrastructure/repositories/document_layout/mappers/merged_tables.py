from typing import Any, Mapping

from deps_document_layout.model import MergedTable, ParsingType, TableReference

__all__ = ["MergedTablesMapper"]


class MergedTablesMapper:
    @staticmethod
    def to_dict(merged_table: dict[ParsingType, list[MergedTable]]) -> dict[str, Any]:
        return {
            parsing_type.value: [MergedTablesMapper.table_to_dict(table) for table in tables]
            for parsing_type, tables in merged_table.items()
        }

    @staticmethod
    def from_dict(raw_merged_table: Mapping) -> dict[ParsingType, list[MergedTable]]:
        return {
            ParsingType(parsing_type): [MergedTablesMapper.table_from_dict(table) for table in tables]
            for parsing_type, tables in raw_merged_table.items()
        }

    @staticmethod
    def table_to_dict(table: MergedTable) -> dict[str, Any]:
        return {
            "parsing_type": table.parsing_type.value,
            "tables": [
                {
                    "page_number": table_reference.page_number,
                    "table_id": table_reference.table_id,
                }
                for table_reference in table.tables
            ],
        }

    @staticmethod
    def table_from_dict(raw_table: Mapping) -> MergedTable:
        return MergedTable(
            parsing_type=ParsingType(raw_table["parsing_type"]),
            tables=[
                TableReference(
                    page_number=table["page_number"],
                    table_id=table["table_id"],
                )
                for table in raw_table["tables"]
            ],
        )
