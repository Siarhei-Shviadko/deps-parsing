from dataclasses import dataclass

from deps_document_layout.model import MergedTable, ParsingFeatures, ParsingType

__all__ = ["DocumentLayoutInfo", "PageInfo"]


@dataclass
class PageInfo:
    pages_count: int


@dataclass
class DocumentLayoutInfo:
    id: str
    parsing_features: ParsingFeatures
    merged_tables: dict[ParsingType, list[MergedTable]]
    pages_info: dict[ParsingType, PageInfo]
