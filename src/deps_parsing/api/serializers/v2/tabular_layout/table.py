from deps_tabular_layout.serializers import SerializedCell
from pydantic import Field

from deps_parsing.domain.dtos import TableProjection, TableSchemaProjection

from ...base import ConfiguredBaseModel

__all__ = ["SerializedTable"]


class SerializedTableSchema(ConfiguredBaseModel):
    id: str
    sheet_id: str = Field(..., alias="sheetId")
    column_count: int = Field(..., alias="columnCount")
    row_count: int = Field(..., alias="rowCount")
    placement: tuple[dict[str, int], dict[str, int]]

    @classmethod
    def from_model(cls, schema: TableSchemaProjection) -> "SerializedTableSchema":
        return cls(
            id=schema.id,
            sheet_id=schema.sheet_id,
            column_count=schema.column_count,
            row_count=schema.row_count,
            placement=(
                {"column": schema.placement[0].x, "row": schema.placement[0].y},
                {"column": schema.placement[1].x, "row": schema.placement[1].y},
            ),
        )


class SerializedTable(ConfiguredBaseModel):
    schema_: SerializedTableSchema = Field(..., alias="schema")  # noqa: WPS120
    data: list[SerializedCell]

    @classmethod
    def from_model(cls, table: TableProjection) -> "SerializedTable":
        return cls(
            schema_=SerializedTableSchema.from_model(table.schema),
            data=[SerializedCell.from_model(cell) for cell in table.data],
        )
