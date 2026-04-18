from deps_tabular_layout.serializers import SerializedImage
from deps_tabular_layout.serializers import SerializedSheet as BaseSerializedSheet
from pydantic import Field

from deps_parsing.domain.dtos import SheetProjection

__all__ = ["SerializedSheet"]


class SerializedSheet(BaseSerializedSheet):
    table_ids: list[str] = Field(default_factory=list, alias="tableIds")
    tables: None = Field(None, exclude=True)

    @classmethod
    def from_model(cls, sheet: SheetProjection) -> "SerializedSheet":
        return cls(
            id=sheet.id,
            title=sheet.title,
            is_hidden=sheet.is_hidden,
            images=[SerializedImage.from_model(image) for image in sheet.images],
            table_ids=sheet.table_ids,
            tables=None,
        )
