from typing import Optional

from pydantic import Field

from deps_parsing.domain.dtos import ParsingInfo

from ..base import ConfiguredBaseModel
from .document_layout import SerializedDocumentLayoutInfo
from .tabular_layout import SerializerTabularLayoutInfo

__all__ = ["SerializedParsingInfo"]


class SerializedParsingInfo(ConfiguredBaseModel):
    layout_id: str = Field(..., alias="layoutId")
    document_layout_info: Optional[SerializedDocumentLayoutInfo] = Field(..., alias="documentLayoutInfo")
    tabular_layout_info: Optional[SerializerTabularLayoutInfo] = Field(..., alias="tabularLayoutInfo")

    @classmethod
    def from_model(cls, info: ParsingInfo) -> "SerializedParsingInfo":
        return cls(
            layout_id=info.layout_id,
            document_layout_info=(
                SerializedDocumentLayoutInfo.from_model(info.document_layout_info)
                if info.document_layout_info
                else None
            ),
            tabular_layout_info=(
                SerializerTabularLayoutInfo.from_model(info.tabular_layout_info) if info.tabular_layout_info else None
            ),
        )
