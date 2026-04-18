from typing import Any, Mapping

from deps_document_layout.model import (
    DocumentLayout,
    EntityId,
    ParsingFeature,
    ParsingFeatures,
    ParsingType,
    TenantId,
)

from deps_parsing.domain.dtos import DocumentLayoutInfo, PageInfo

from .merged_tables import MergedTablesMapper
from .page import PageMapper

__all__ = ["DocumentLayoutMapper", "ParsingFeaturesMapper"]


class DocumentLayoutMapper:
    @classmethod
    def to_dict(cls, document_layout: DocumentLayout) -> dict[str, Any]:
        return {
            "document_layout": {
                "id": document_layout.id(),
                "tenant_id": document_layout.tenant_id(),
                "parsing_features": ParsingFeaturesMapper.to_dict(document_layout.parsing_features),
                "merged_tables": MergedTablesMapper.to_dict(document_layout.merged_tables),
            },
            "pages": PageMapper.to_dict(document_layout.id(), document_layout.pages),
        }

    @classmethod
    def from_dict(cls, raw_document_layout: Mapping) -> DocumentLayout:
        return DocumentLayout(
            id_=EntityId(raw_document_layout["id"]),
            tenant_id=TenantId(raw_document_layout["tenant_id"]),
            parsing_features=ParsingFeaturesMapper.from_dict(raw_document_layout["parsing_features"]),
            pages=(
                [PageMapper.from_dict(page) for page in raw_document_layout["pages"]]
                if "pages" in raw_document_layout
                else None
            ),
            merged_tables=MergedTablesMapper.from_dict(raw_merged_table=raw_document_layout["merged_tables"]),
        )

    @classmethod
    def layout_info_from_dict(cls, raw_dl: Mapping, pages_count_result: list[Mapping]) -> DocumentLayoutInfo:
        return DocumentLayoutInfo(
            id=raw_dl["id"],
            pages_info={
                ParsingType(row["parsing_type"]): PageInfo(pages_count=row["page_amount"]) for row in pages_count_result
            },
            merged_tables=MergedTablesMapper.from_dict(raw_dl["merged_tables"]),
            parsing_features=ParsingFeaturesMapper.from_dict(raw_dl["parsing_features"]),
        )


class ParsingFeaturesMapper:
    @classmethod
    def to_dict(cls, parsing_features: ParsingFeatures) -> dict[str, Any]:
        return {
            parsing_type.value: [feature.value for feature in features]
            for parsing_type, features in parsing_features.items()
        }

    @classmethod
    def from_dict(cls, raw_parsing_features: Mapping) -> ParsingFeatures:
        return {
            ParsingType(parsing_type): {ParsingFeature(feature) for feature in features}
            for parsing_type, features in raw_parsing_features.items()
        }
