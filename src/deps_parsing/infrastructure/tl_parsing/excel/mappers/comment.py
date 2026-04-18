from typing import Optional

import openpyxl as xl
from deps_tabular_layout.models import CommentInput

__all__ = ["CommentMapper"]


class CommentMapper:
    @staticmethod
    def from_cell(cell: xl.cell.cell.Cell) -> Optional[CommentInput]:
        if cell.comment is None:
            return None

        return CommentInput(
            author=cell.comment.author,
            content=cell.comment.content,
        )
