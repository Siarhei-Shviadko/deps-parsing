from typing import Any, Optional, Protocol, TypeVar

__all__ = ["ICanParseDocument"]


FeatureType = TypeVar("FeatureType")
ParsingType = TypeVar("ParsingType", contravariant=True)
EntityId = TypeVar("EntityId", covariant=True)


class ICanParseDocument(Protocol[FeatureType, ParsingType, EntityId]):
    def parse(
        self,
        entity_id: str,
        tenant_id: str,
        file_path: str,
        parsing_type: ParsingType,
        features: Optional[set[FeatureType]] = None,
        language: Optional[str] = None,
        routing_info: Optional[dict[str, Any]] = None,
    ) -> EntityId:
        pass
