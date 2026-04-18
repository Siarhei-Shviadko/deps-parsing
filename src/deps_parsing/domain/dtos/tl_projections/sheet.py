from dataclasses import dataclass

from deps_tabular_layout.models import Image

__all__ = ["SheetProjection"]


@dataclass
class SheetProjection:
    id: str
    title: str
    images: list[Image]
    is_hidden: bool
    table_ids: list[str]
