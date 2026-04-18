import io
from typing import Iterator

import chardet
from deps_tabular_layout.models import (
    Cell,
    DataType,
    PositionInput,
    TableBuilder,
    TabularLayout,
)

from ...csv import CsvReader
from ..abstract_parser import AbstractTabularLayoutParser

__all__ = ["CSVParser"]

DEFAULT_TITLE = "CSV Table"
DEFAULT_ENCODING = "utf-8"
START_X_POSITION = 0
START_Y_POSITION = 0
DEFAULT_VISIBILITY = True


class CSVParser(AbstractTabularLayoutParser):
    _CELL_BATCH_SIZE = 100

    def _perform_parsing(self, blob: bytes, tabular_layout: TabularLayout) -> TabularLayout:
        encoding = chardet.detect(blob).get("encoding") or DEFAULT_ENCODING
        with io.StringIO(blob.decode(encoding=encoding, errors="ignore")) as f:
            return self._add_table(tabular_layout=tabular_layout, reader=CsvReader(f))

    def _add_table(self, tabular_layout: TabularLayout, reader: CsvReader) -> TabularLayout:
        builder = (
            tabular_layout.with_sheet()
            .with_title(DEFAULT_TITLE)
            .with_visibility(DEFAULT_VISIBILITY)
            .with_table(
                left_top_corner=(START_X_POSITION, START_Y_POSITION),
                right_bottom_corner=reader.table_size,
            )
        )

        builder = self._add_data_to_table(layout_id=tabular_layout.id(), builder=builder, rows=reader.rows)
        builder.build()

        return tabular_layout

    def _add_data_to_table(self, layout_id: str, builder: TableBuilder, rows: Iterator[list[str]]) -> TableBuilder:
        cells_batch: list[Cell] = []

        for row_ind, row_data in enumerate(rows):
            for col_ind, col_data in enumerate(row_data):
                cells_batch.append(
                    builder.record_cell(
                        content=col_data,
                        data_type=DataType.STRING,
                        position=PositionInput(
                            relative_position=(col_ind, row_ind),
                            absolute_position=(col_ind, row_ind),
                        ),
                    ),
                )
                if self._is_batch_ready(cells_batch):
                    self._cell_repository.save_batch(layout_id, cells_batch)
                    cells_batch.clear()

        if cells_batch:
            self._cell_repository.save_batch(layout_id, cells_batch)

        return builder

    def _is_batch_ready(self, batch: list[Cell]) -> bool:
        return len(batch) >= self._CELL_BATCH_SIZE
