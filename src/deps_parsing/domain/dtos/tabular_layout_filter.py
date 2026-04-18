from dataclasses import dataclass
from typing import Optional

__all__ = ["TabularLayoutFilter"]


@dataclass
class TabularLayoutFilter:
    tables: Optional[list[str]] = None
    row_span: Optional[tuple[int, int]] = None
    col_span: Optional[tuple[int, int]] = None
