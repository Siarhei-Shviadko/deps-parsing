from deps_document_layout.serializers.document_layout.merged_table import (
    SerializedMergedTable,
)
from pydantic import Field

from deps_parsing.domain.dtos import DocumentLayoutInfo

from ....base import ConfiguredBaseModel
from .page_info import SerializedPageInfo

__all__ = ["SerializedDocumentLayoutInfo"]

SerializedParsingFeatures = dict[str, list[str]]
SerializedMergedTables = dict[str, list[SerializedMergedTable]]
SerializedPagesInfo = dict[str, SerializedPageInfo]


class SerializedDocumentLayoutInfo(ConfiguredBaseModel):
    id: str = Field(..., alias="documentLayoutId")
    parsing_features: SerializedParsingFeatures = Field(..., alias="parsingFeatures")
    merged_tables: SerializedMergedTables = Field(None, alias="mergedTables")
    pages_info: SerializedPagesInfo = Field(None, alias="pagesInfo")

    @classmethod
    def from_model(cls, document_layout: DocumentLayoutInfo) -> "SerializedDocumentLayoutInfo":
        return cls(
            id=document_layout.id,
            parsing_features=document_layout.parsing_features,
            merged_tables={
                parsing_type: [SerializedMergedTable.from_model(table) for table in merged_tables]
                for parsing_type, merged_tables in document_layout.merged_tables.items()
            },
            pages_info={
                parsing_type: SerializedPageInfo.from_model(page_info)
                for parsing_type, page_info in document_layout.pages_info.items()
            },
        )
