from deps_document_layout.model import EntityId, Paragraph, ParsingType, RawParagraph

from .line import LineMapper
from .polygon import PointMapper

__all__ = ["ParagraphMapper"]


class ParagraphMapper:
    @classmethod
    def to_dict(cls, paragraph: Paragraph, page_id: str, parsing_type: ParsingType) -> RawParagraph:
        return {
            "id": paragraph.id(),
            "order_num": paragraph.order,
            "content": paragraph.content,
            "confidence": paragraph.confidence,
            "role": paragraph.role,
            "polygon": [PointMapper.to_dict(point) for point in paragraph.polygon],
            "lines": [LineMapper.to_dict(line) for line in paragraph.lines],
            "page_id": page_id,
            "parsing_type": parsing_type,
        }

    @classmethod
    def from_dict(cls, paragraph: RawParagraph) -> Paragraph:
        return Paragraph(
            id_=EntityId(paragraph["id"]),
            order=paragraph["order_num"],
            content=paragraph["content"],
            confidence=float(confidence) if (confidence := paragraph["confidence"]) is not None else None,
            role=paragraph["role"],
            polygon=tuple(PointMapper.from_dict(point) for point in paragraph["polygon"]),
            lines=tuple(LineMapper.from_dict(line) for line in paragraph["lines"]),
        )
