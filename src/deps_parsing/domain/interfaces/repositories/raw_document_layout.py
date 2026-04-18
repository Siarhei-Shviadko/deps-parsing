from abc import ABC, abstractmethod
from typing import Any

from deps_document_layout.model import ParsingType

__all__ = ["IRawDocumentLayoutRepository"]


class IRawDocumentLayoutRepository(ABC):
    @abstractmethod
    def save(self, layout_id: str, layout: dict[str, Any], parsing_type: ParsingType) -> None:
        ...

    @abstractmethod
    def layout_of_id(self, layout_id: str, parsing_type: ParsingType) -> dict[str, Any]:
        ...
