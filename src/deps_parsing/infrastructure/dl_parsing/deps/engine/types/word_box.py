from dataclasses import dataclass

from .bbox import Bbox

__all__ = ["WordBox"]


@dataclass(frozen=True)
class WordBox:
    content: str
    bbox: Bbox
    confidence: float

    @classmethod
    def from_dict(cls, **kwargs) -> "WordBox":
        return cls(
            content=kwargs["content"],
            bbox=Bbox(**kwargs["bbox"]),
            confidence=kwargs["confidence"],
        )
