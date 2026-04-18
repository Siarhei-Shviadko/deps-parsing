from deps_document_layout.model import (
    EntityId,
    KeyValuePair,
    KeyValuePairElement,
    ParsingType,
    RawKeyValueElement,
    RawKeyValuePair,
)

from .polygon import PolygonMapper

__all__ = ["KeyValuePairMapper"]


class KeyValuePairMapper:
    @classmethod
    def to_dict(cls, kv_pair: KeyValuePair, page_id: str, parsing_type: ParsingType) -> RawKeyValuePair:
        return {
            "id": kv_pair.id(),
            "order_num": kv_pair.order,
            "key": cls._key_value_element_to_dict(kv_pair.key),
            "value": cls._key_value_element_to_dict(kv_pair.value) if kv_pair.value else None,
            "confidence": kv_pair.confidence,
            "page_id": page_id,
            "parsing_type": parsing_type,
        }

    @classmethod
    def from_dict(cls, kv_pair: RawKeyValuePair) -> KeyValuePair:
        return KeyValuePair(
            id_=EntityId(kv_pair["id"]),
            order=kv_pair["order_num"],
            key=cls._key_value_element_from_dict(kv_pair["key"]),
            value=cls._key_value_element_from_dict(kv_pair["value"]) if kv_pair["value"] is not None else None,
            confidence=float(kv_pair["confidence"]),
        )

    @classmethod
    def _key_value_element_to_dict(cls, element: KeyValuePairElement) -> RawKeyValueElement:
        return {
            "content": element.content,
            "polygon": PolygonMapper.to_dict(element.polygon),
            "paragraph_id": element.paragraph_id() if element.paragraph_id else None,
        }

    @classmethod
    def _key_value_element_from_dict(cls, element: RawKeyValueElement) -> KeyValuePairElement:
        return KeyValuePairElement(
            content=element["content"],
            polygon=PolygonMapper.from_dict(element["polygon"]),
            paragraph_id=EntityId(element["paragraph_id"]) if element["paragraph_id"] else None,
        )
