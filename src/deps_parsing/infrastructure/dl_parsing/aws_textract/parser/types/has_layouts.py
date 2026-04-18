from typing import Protocol

from textractor.entities.layout import Layout

__all__ = ["HasLayouts"]


class HasLayouts(Protocol):
    @property
    def layouts(self) -> list[Layout]:
        pass
