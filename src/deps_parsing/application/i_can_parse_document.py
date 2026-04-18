from typing import Optional, Protocol, TypeVar

__all__ = ["ICanParseDocument"]


FeatureType = TypeVar("FeatureType")
ParsingType = TypeVar("ParsingType", contravariant=True)
EntityId = TypeVar("EntityId", covariant=True)


class ICanParseDocument(Protocol[FeatureType, ParsingType, EntityId]):
    def parse(
        self,
        document_id: str,
        tenant_id: str,
        parsing_type: ParsingType,
        features: Optional[set[FeatureType]] = None,
        language: Optional[str] = None,
    ) -> EntityId:
        pass
