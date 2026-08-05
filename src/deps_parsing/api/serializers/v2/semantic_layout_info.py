from datetime import datetime
from typing import Optional

from pydantic import Field

from deps_parsing.domain.dtos import SemanticLayoutInfo, SemanticLayoutMetadataInfo

from ..base import ConfiguredBaseModel

__all__ = ["SerializedSemanticLayoutMetadataInfo", "SerializedSemanticLayoutInfo"]


class SerializedSemanticLayoutMetadataInfo(ConfiguredBaseModel):
    source_provider: str = Field(..., alias="sourceProvider")
    processing_time_ms: Optional[int] = Field(None, alias="processingTimeMs")
    confidence: Optional[float] = None

    @classmethod
    def from_model(cls, metadata: SemanticLayoutMetadataInfo) -> "SerializedSemanticLayoutMetadataInfo":
        return cls(
            source_provider=metadata.source_provider,
            processing_time_ms=metadata.processing_time_ms,
            confidence=metadata.confidence,
        )


class SerializedSemanticLayoutInfo(ConfiguredBaseModel):
    id: str
    provider: str
    created_at: datetime = Field(..., alias="createdAt")
    metadata: SerializedSemanticLayoutMetadataInfo

    @classmethod
    def from_model(cls, info: SemanticLayoutInfo) -> "SerializedSemanticLayoutInfo":
        return cls(
            id=info.id,
            provider=info.provider,
            created_at=info.created_at,
            metadata=SerializedSemanticLayoutMetadataInfo.from_model(info.metadata),
        )
