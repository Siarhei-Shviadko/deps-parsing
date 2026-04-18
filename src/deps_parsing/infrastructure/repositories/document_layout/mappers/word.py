from deps_document_layout.model import RawStyle, RawWord, Style, Word

from .base_element import BaseLineElementMapper

__all__ = ["WordMapper"]


class WordMapper:
    @classmethod
    def to_dict(cls, word: Word) -> RawWord:
        return {
            "content": word.content,
            "style": cls._style_to_dict(word.style),
            **BaseLineElementMapper.to_dict(word),
        }

    @classmethod
    def from_dict(cls, word: RawWord) -> Word:
        return Word(
            content=word["content"],
            style=cls._style_from_dict(word["style"]),
            **BaseLineElementMapper.from_dict(word),
        )

    @classmethod
    def _style_to_dict(cls, style: Style) -> RawStyle:
        return {
            "background_color": style.background_color,
            "color": style.color,
            "bold": style.bold,
            "italic": style.italic,
            "handwritten": style.handwritten,
            "font_type": style.font_type,
            "font_size": style.font_size,
            "underlined": style.underlined,
            "strikeout": style.strikeout,
            "subscript": style.subscript,
            "superscript": style.superscript,
            "smallcaps": style.smallcaps,
        }

    @classmethod
    def _style_from_dict(cls, style: RawStyle) -> Style:
        return Style(
            background_color=style["background_color"],
            color=style["color"],
            bold=style["bold"],
            italic=style["italic"],
            handwritten=style["handwritten"],
            font_type=style["font_type"],
            font_size=style["font_size"],
            underlined=style["underlined"],
            strikeout=style["strikeout"],
            subscript=style["subscript"],
            superscript=style["superscript"],
            smallcaps=style["smallcaps"],
        )
