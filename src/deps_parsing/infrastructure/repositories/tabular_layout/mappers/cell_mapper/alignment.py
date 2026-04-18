from typing import Any

from deps_tabular_layout.models import Alignment

__all__ = ["AlignmentMapper"]


class AlignmentMapper:
    @staticmethod
    def to_dict(alignment: Alignment) -> dict[str, Any]:
        return {
            "horizontal": alignment.horizontal,
            "vertical": alignment.vertical,
            "rotation": alignment.rotation,
        }

    @staticmethod
    def from_raw(raw_data: dict[str, Any]) -> Alignment:
        return Alignment(
            horizontal=raw_data["horizontal"],
            vertical=raw_data["vertical"],
            rotation=raw_data["rotation"],
        )
