from dataclasses import dataclass

from deps_document_layout.model import Polygon

__all__ = ["ParsedImage"]


@dataclass
class ParsedImage:
    title: str
    description: str
    filepath: str
    page_coordinates: Polygon

    def with_updated_annotations(self, title: str, description: str) -> "ParsedImage":
        self.title = title
        self.description = description

        return self
