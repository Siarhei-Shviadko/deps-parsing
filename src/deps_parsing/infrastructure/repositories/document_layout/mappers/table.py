from deps_document_layout.model import (
    Cell,
    EntityId,
    ParsingType,
    RawCell,
    RawTable,
    Table,
)

from .polygon import PolygonMapper

__all__ = ["TableMapper"]


class TableMapper:
    @classmethod
    def to_dict(cls, table: Table, page_id: str, parsing_type: ParsingType) -> RawTable:
        return {
            "id": table.id(),
            "order_num": table.order,
            "cells": [cls._cell_to_dict(cell) for cell in table.cells],
            "confidence": table.confidence,
            "column_count": table.column_count,
            "row_count": table.row_count,
            "polygon": PolygonMapper.to_dict(table.polygon),
            "page_id": page_id,
            "parsing_type": parsing_type,
        }

    @classmethod
    def from_dict(cls, table: RawTable) -> Table:
        return Table(
            id_=EntityId(table["id"]),
            order=table["order_num"],
            cells=tuple(cls._cell_from_dict(cell) for cell in table["cells"]),
            confidence=float(confidence) if (confidence := table["confidence"]) is not None else None,
            column_count=table["column_count"],
            row_count=table["row_count"],
            polygon=PolygonMapper.from_dict(table["polygon"]),
        )

    @classmethod
    def _cell_to_dict(cls, cell: Cell) -> RawCell:
        return {
            "content": cell.content,
            "kind": cell.kind,
            "column_index": cell.column_index,
            "column_span": cell.column_span,
            "row_index": cell.row_index,
            "row_span": cell.row_span,
            "polygon": PolygonMapper.to_dict(cell.polygon),
            "paragraph_id": cell.paragraph_id() if cell.paragraph_id else None,
        }

    @classmethod
    def _cell_from_dict(cls, cell: RawCell) -> Cell:
        return Cell(
            content=cell["content"],
            kind=cell["kind"],
            column_index=cell["column_index"],
            column_span=cell["column_span"],
            row_index=cell["row_index"],
            row_span=cell["row_span"],
            polygon=PolygonMapper.from_dict(cell["polygon"]),
            paragraph_id=EntityId(cell["paragraph_id"]) if cell["paragraph_id"] else None,
        )
