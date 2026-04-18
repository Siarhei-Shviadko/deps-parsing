from typing import Any

from deps_tabular_layout.models import Style

__all__ = ["StyleMapper"]


class StyleMapper:
    @staticmethod
    def to_dict(style: Style) -> dict[str, Any]:
        return {
            "background_color": style.background_color,
            "color": style.color,
            "hyperlink": style.hyperlink,
            "bold": style.bold,
            "italic": style.italic,
            "font_name": style.font_name,
            "font_size": style.font_size,
            "underlined": style.underlined,
            "strikethrough": style.strikethrough,
        }

    @staticmethod
    def from_raw(raw_data: dict[str, Any]) -> Style:
        return Style(
            background_color=raw_data["background_color"],
            color=raw_data["color"],
            hyperlink=raw_data["hyperlink"],
            bold=raw_data["bold"],
            italic=raw_data["italic"],
            font_name=raw_data["font_name"],
            font_size=raw_data["font_size"],
            underlined=raw_data["underlined"],
            strikethrough=raw_data["strikethrough"],
        )
