from pydantic import Field

from deps_parsing.domain.dtos import SheetInfo, TableInfo, TabularLayoutInfo

from ...base import ConfiguredBaseModel

__all__ = ["SerializerTabularLayoutInfo"]


class SerializedTableInfo(ConfiguredBaseModel):
    id: str
    row_count: int = Field(..., alias="rowCount")
    column_count: int = Field(..., alias="columnCount")

    @classmethod
    def from_model(cls, table: TableInfo) -> "SerializedTableInfo":
        return cls(
            id=table.id,
            row_count=table.row_count,
            column_count=table.column_count,
        )


class SerializedSheetInfo(ConfiguredBaseModel):
    id: str
    title: str
    is_hidden: bool = Field(..., alias="isHidden")
    tables: list[SerializedTableInfo]
    images: list[str]

    @classmethod
    def from_model(cls, sheet: SheetInfo) -> "SerializedSheetInfo":
        return cls(
            id=sheet.id,
            title=sheet.title,
            is_hidden=sheet.is_hidden,
            tables=[SerializedTableInfo.from_model(table) for table in sheet.tables],
            images=sheet.images,
        )


class SerializerTabularLayoutInfo(ConfiguredBaseModel):
    id: str
    parsing_type: str = Field(..., alias="parsingType")
    sheets: list[SerializedSheetInfo]

    @classmethod
    def from_model(cls, layout: TabularLayoutInfo) -> "SerializerTabularLayoutInfo":
        return cls(
            id=layout.id,
            parsing_type=layout.parsing_type.value,
            sheets=[SerializedSheetInfo.from_model(sheet) for sheet in layout.sheets],
        )
