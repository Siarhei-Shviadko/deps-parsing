from dataclasses import dataclass

from .word_box import WordBox

__all__ = ["TextLine"]


@dataclass(frozen=True)
class TextLine:
    id: int
    word_boxes: list[WordBox]

    @classmethod
    def from_dict(cls, **kwargs) -> "TextLine":
        return cls(id=kwargs["id"], word_boxes=[WordBox.from_dict(**word_box) for word_box in kwargs["wordBoxes"]])
