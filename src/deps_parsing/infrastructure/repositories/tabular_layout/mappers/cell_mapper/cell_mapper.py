from typing import Any

from deps_tabular_layout.models import Cell, DataType, EntityId

from .absolute_position import AbsolutePositionMapper
from .alignment import AlignmentMapper
from .borders import BordersMapper
from .comment import CommentMapper
from .merge_info import MergeInfoMapper
from .relative_position import RelativePositionMapper
from .style import StyleMapper

__all__ = ["CellMapper"]


class CellMapper:
    @staticmethod
    def to_dict(layout_id: str, cell: Cell) -> dict[str, Any]:
        return {
            "id": cell.id(),
            "tabular_layout_id": layout_id,
            "table_id": cell.table_id(),
            "content": cell.content,
            "data_type": cell.data_type,
            "relative_position_row": cell.relative_position.y,
            "relative_position_column": cell.relative_position.x,
            "absolute_position_row": cell.absolute_position.y,
            "absolute_position_column": cell.absolute_position.x,
            "merge": MergeInfoMapper.to_dict(cell.merge) if cell.merge is not None else None,
            "style": StyleMapper.to_dict(cell.style) if cell.style is not None else None,
            "comment": CommentMapper.to_dict(cell.comment) if cell.comment is not None else None,
            "alignment": AlignmentMapper.to_dict(cell.alignment) if cell.alignment is not None else None,
            "borders": BordersMapper.to_dict(cell.borders) if cell.borders is not None else None,
        }

    @staticmethod
    def from_raw(raw_cell: dict[str, Any]) -> Cell:
        return Cell(
            id_=EntityId(raw_cell["id"]),
            table_id=EntityId(raw_cell["table_id"]),
            content=raw_cell["content"],
            relative_position=RelativePositionMapper.from_raw(raw_cell),
            absolute_position=AbsolutePositionMapper.from_raw(raw_cell),
            data_type=DataType(raw_cell["data_type"]),
            merge=MergeInfoMapper.from_raw(raw_cell["merge"]) if raw_cell["merge"] is not None else None,
            style=StyleMapper.from_raw(raw_cell["style"]) if raw_cell["style"] is not None else None,
            comment=CommentMapper.from_raw(raw_cell["comment"]) if raw_cell["comment"] is not None else None,
            alignment=AlignmentMapper.from_raw(raw_cell["alignment"]) if raw_cell["alignment"] is not None else None,
            borders=BordersMapper.from_raw(raw_cell["borders"]) if raw_cell["borders"] is not None else None,
        )
