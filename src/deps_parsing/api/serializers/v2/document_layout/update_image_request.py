from typing import Optional

from deps_document_layout.model import RawPolygon

from ...base import ConfiguredBaseModel

__all__ = ["UpdateImageRequest"]


class UpdateImageRequest(ConfiguredBaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    filepath: Optional[str] = None
    polygon: Optional[RawPolygon] = None
