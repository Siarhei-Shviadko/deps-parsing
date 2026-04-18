from dataclasses import dataclass

from .bbox import Bbox

__all__ = ["SourceBboxCoordinates"]


@dataclass(frozen=True)
class SourceBboxCoordinates:
    source_id: str
    bboxes: list[Bbox]

    @classmethod
    def from_dict(cls, **kwargs) -> "SourceBboxCoordinates":
        return cls(source_id=kwargs["sourceId"], bboxes=[Bbox(**word_box) for word_box in kwargs["bboxes"]])
