from typing import Optional

import pytest
from deps_tabular_layout.models import Cell, DataType, Point

from deps_parsing.infrastructure.tl_parsing import ExcelParser
from tests.fakes import FakeCellCommandRepository, FakeDocumentProxy


def _get_cell_by_position(cells: dict[str, Cell], position: Point) -> Optional[Cell]:
    return next(filter(lambda c: c.absolute_position == position, cells.values()), None)


def _load_excel_file(file_path: str) -> bytes:
    with open(file_path, "rb") as file:
        return file.read()


def test_parsing_excel_file__all_styles(
    excel_file_bytes__all_styles: bytes,
    empty_tabular_layout,
    fake_cell_command_repository: FakeCellCommandRepository,
    fake_document_proxy: FakeDocumentProxy,
    excel_parser_with_fakes: ExcelParser,
) -> None:
    fake_document_proxy.set_mocked_file(excel_file_bytes__all_styles)

    tl = excel_parser_with_fakes.parse(empty_tabular_layout)

    assert len(tl.sheets) == 1

    sheet = tl.sheets[0]

    assert sheet.title == "tables"
    assert sheet.is_hidden is False
    assert len(sheet.tables) == 3

    table1 = sheet.tables[0]

    assert table1.row_count == 8
    assert table1.column_count == 4
    assert table1.placement == (Point(0, 0), Point(3, 7))

    assert sheet.tables[1].placement == (Point(0, 10), Point(2, 12))
    assert sheet.tables[2].placement == (Point(1, 17), Point(1, 21))

    cells = fake_cell_command_repository.local_db()

    assert len(cells) == 48 - 3 - 1  # 48 cells in total, but - 4merged = 1, 2merged = 1

    merged_cell = _get_cell_by_position(cells, Point(2, 10))
    assert merged_cell
    assert merged_cell.content == "merged"

    styled_cell = _get_cell_by_position(cells, Point(0, 0))
    assert styled_cell
    assert styled_cell.style.bold is True
    assert styled_cell.style.italic is True

    first_cell = cells[next(iter(cells.keys()))]
    assert (first_cell.relative_position.x, first_cell.relative_position.y) == (0, 0)
    assert (first_cell.absolute_position.x, first_cell.absolute_position.y) == (0, 0)

    formula_cell = _get_cell_by_position(cells, Point(0, 12))
    assert formula_cell.content == "7"
    assert formula_cell.data_type == DataType.NUMERIC

    hyperlink_cell = _get_cell_by_position(cells, Point(1, 12))
    assert hyperlink_cell.style.hyperlink is True

    left_bordered = _get_cell_by_position(cells, Point(3, 7))
    assert left_bordered.borders.left
    assert not left_bordered.borders.right
    assert not left_bordered.borders.bottom
    assert not left_bordered.borders.top


@pytest.mark.parametrize(
    "file_path,expected_sheet_names",
    [
        (
            "tests/data/excel/2-sheets-claim-example.xlsx",
            ["Report", "Claimants", "Sheet1"],
        ),  # there's hidden empty sheet
        ("tests/data/excel/2-sheets-complex-case--empty-sheet.xlsx", ["Rev 27 JAN2014", "empty"]),
        (
            "tests/data/excel/2-sheets-whole-sheet-as-table.xlsx",
            ["whole-sheet-as-table", "whole-sheet-split-by-row-only"],
        ),
    ],
)
def test_parsing_complex_cases__no_error_occur(
    file_path: str,
    expected_sheet_names: list[str],
    empty_tabular_layout,
    fake_cell_command_repository: FakeCellCommandRepository,
    fake_document_proxy: FakeDocumentProxy,
    excel_parser_with_fakes: ExcelParser,
) -> None:
    excel_file_bytes = _load_excel_file(file_path)
    fake_document_proxy.set_mocked_file(excel_file_bytes)

    tl = excel_parser_with_fakes.parse(empty_tabular_layout)

    assert len(tl.sheets) == len(expected_sheet_names)

    for sheet, expected_name in zip(tl.sheets, expected_sheet_names):
        assert sheet.title == expected_name


def test_parsing_excel_file__large_file_batch_cells_saving(
    excel_file_bytes__large_table: bytes,
    empty_tabular_layout,
    cell_command_repository_mock,
    fake_document_proxy: FakeDocumentProxy,
    excel_parser_with_mocked_repo: ExcelParser,
) -> None:
    fake_document_proxy.set_mocked_file(excel_file_bytes__large_table)

    tl = excel_parser_with_mocked_repo.parse(empty_tabular_layout)

    assert len(tl.sheets) == 1

    sheet = tl.sheets[0]
    assert len(sheet.tables) == 1
    assert cell_command_repository_mock.save_batch.call_count == 25
