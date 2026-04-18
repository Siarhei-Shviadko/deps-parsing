from collections import namedtuple
from dataclasses import dataclass, field

from deps_document_layout.model import (
    ParsingType,
    RawMergedTable,
    RawTableReference,
    Table,
)

__all__ = ["TablesGroup"]

TableRef = namedtuple("TableRef", ["page_number", "table_id"])


@dataclass
class TablesGroup:
    parsing_type: ParsingType
    tables: set[TableRef] = field(default_factory=set)

    def has_tables(self) -> bool:
        return bool(self.tables)

    def add(self, for_page: int, table: Table) -> None:
        self.tables.add(TableRef(page_number=for_page, table_id=table.id()))

    def to_raw(self) -> RawMergedTable:
        return {
            "parsing_type": self.parsing_type,
            "tables": self.tables_references(),
        }

    def tables_references(self) -> list[RawTableReference]:
        return [RawTableReference(page_number=page_number, table_id=table_id) for page_number, table_id in self.tables]
