from deps_tabular_layout.models import Borders

__all__ = ["BordersMapper"]


class BordersMapper:
    @staticmethod
    def to_dict(borders: Borders) -> dict[str, str]:
        return {
            "left": borders.left,
            "right": borders.right,
            "top": borders.top,
            "bottom": borders.bottom,
        }

    @staticmethod
    def from_raw(raw_data: dict[str, str]) -> Borders:
        return Borders(
            left=raw_data["left"],
            right=raw_data["right"],
            top=raw_data["top"],
            bottom=raw_data["bottom"],
        )
