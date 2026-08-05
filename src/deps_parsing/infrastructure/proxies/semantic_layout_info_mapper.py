from datetime import datetime
from typing import Any

from deps_parsing.domain.dtos import SemanticLayoutInfo, SemanticLayoutMetadataInfo

__all__ = ["SemanticLayoutInfoMapper"]


class SemanticLayoutInfoMapper:
    @staticmethod
    def from_dict(payload: dict[str, Any], layout_id: str) -> SemanticLayoutInfo:
        metadata_payload = payload.get("metadata") or {}
        return SemanticLayoutInfo(
            id=payload.get("id") or layout_id,
            provider=payload["provider"],
            created_at=SemanticLayoutInfoMapper._parse_datetime(payload["createdAt"]),  # noqa: WPS437
            metadata=SemanticLayoutMetadataInfo(
                source_provider=metadata_payload["sourceProvider"],
                processing_time_ms=metadata_payload.get("processingTimeMs"),
                confidence=metadata_payload.get("confidence"),
            ),
        )

    @staticmethod
    def from_all_providers_dict(payload: dict[str, Any], layout_id: str) -> dict[str, SemanticLayoutInfo]:
        semantic_layout_info = payload.get("semanticLayoutInfo") or {}
        return {
            provider: SemanticLayoutInfoMapper.from_dict(info, layout_id)
            for provider, info in semantic_layout_info.items()
        }

    @staticmethod
    def _parse_datetime(value: str) -> datetime:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
