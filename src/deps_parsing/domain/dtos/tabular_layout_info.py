from dataclasses import dataclass

from deps_tabular_layout.models import ParsingType

__all__ = ["TabularLayoutInfo", "SheetInfo", "TableInfo"]


@dataclass
class TableInfo:
    id: str
    row_count: int
    column_count: int


@dataclass
class SheetInfo:
    id: str
    title: str
    is_hidden: bool
    tables: list[TableInfo]
    images: list[str]


@dataclass
class TabularLayoutInfo:
    id: str
    parsing_type: ParsingType
    sheets: list[SheetInfo]
