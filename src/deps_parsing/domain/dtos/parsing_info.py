from dataclasses import dataclass
from typing import Optional

from .document_layout_info import DocumentLayoutInfo
from .tabular_layout_info import TabularLayoutInfo

__all__ = ["ParsingInfo"]


@dataclass
class ParsingInfo:
    layout_id: str
    document_layout_info: Optional[DocumentLayoutInfo]
    tabular_layout_info: Optional[TabularLayoutInfo]
