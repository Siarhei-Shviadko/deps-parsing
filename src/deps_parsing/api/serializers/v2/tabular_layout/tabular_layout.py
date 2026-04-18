from pydantic import Field

from deps_parsing.domain.dtos import TabularLayoutProjection

from ...base import ConfiguredBaseModel
from .sheet import SerializedSheet
from .table import SerializedTable

__all__ = ["SerializedTabularLayout"]


class SerializedTabularLayout(ConfiguredBaseModel):
    id: str
    tenant_id: str = Field(..., alias="tenantId")
    parsing_type: str = Field(..., alias="parsingType")
    extracted_properties: list[str] = Field(default_factory=list, alias="extractedProperties")
    sheets: dict[str, SerializedSheet]
    tables: dict[str, SerializedTable]

    @classmethod
    def from_model(cls, tl: TabularLayoutProjection) -> "SerializedTabularLayout":
        return cls(
            id=tl.id,
            tenant_id=tl.tenant_id,
            parsing_type=tl.parsing_type,
            extracted_properties=list(tl.extracted_properties),
            sheets={sheet.id: SerializedSheet.from_model(sheet) for sheet in tl.sheets},
            tables={table.schema.id: SerializedTable.from_model(table) for table in tl.tables},
        )
