from dataclasses import dataclass, field

from deps_tabular_layout.models import CellProperties, ParsingType

from .sheet import SheetProjection
from .table import TableProjection

__all__ = ["TabularLayoutProjection"]


@dataclass
class TabularLayoutProjection:
    id: str
    tenant_id: str
    parsing_type: ParsingType
    extracted_properties: list[CellProperties] = field(default_factory=list)
    sheets: list[SheetProjection] = field(default_factory=list)
    tables: list[TableProjection] = field(default_factory=list)
