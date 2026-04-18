from deps_document_layout.model import CellUpdateData
from deps_document_layout.serializers.document_layout import SerializedCellUpdateData

from ...base import ConfiguredBaseModel

__all__ = ["UpdateTableRequest"]


class UpdateTableRequest(ConfiguredBaseModel):
    cells: list[SerializedCellUpdateData]

    @property
    def update_data(self) -> list[CellUpdateData]:
        return [
            CellUpdateData(
                content=cell.content,
                row_index=cell.row_index,
                column_index=cell.column_index,
            )
            for cell in self.cells
        ]
