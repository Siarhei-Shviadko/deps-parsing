from dataclasses import dataclass

from deps_document_layout.model import Polygon

__all__ = ["PreparsedImage"]


@dataclass
class PreparsedImage:
    layout_id: str
    page_image: bytes
    polygon: Polygon
