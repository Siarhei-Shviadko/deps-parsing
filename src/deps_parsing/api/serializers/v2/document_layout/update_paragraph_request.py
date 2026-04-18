from deps_document_layout.model import LineUpdateData
from deps_document_layout.serializers.document_layout import SerializedLineUpdateData

from ...base import ConfiguredBaseModel

__all__ = ["UpdateParagraphRequest"]


class UpdateParagraphRequest(ConfiguredBaseModel):
    lines: list[SerializedLineUpdateData]

    @property
    def update_data(self) -> list[LineUpdateData]:
        return [
            LineUpdateData(
                content=line.content,
                polygon=tuple(point.to_model() for point in line.polygon),
                order=line.order,
            )
            for line in self.lines
        ]
