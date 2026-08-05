from dataclasses import dataclass
from datetime import datetime
from typing import Optional

__all__ = ["SemanticLayoutMetadataInfo", "SemanticLayoutInfo"]


@dataclass
class SemanticLayoutMetadataInfo:
    source_provider: str
    processing_time_ms: Optional[int]
    confidence: Optional[float]


@dataclass
class SemanticLayoutInfo:
    id: str
    provider: str
    created_at: datetime
    metadata: SemanticLayoutMetadataInfo
