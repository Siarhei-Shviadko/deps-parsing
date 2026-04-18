import openpyxl as xl
import pytest

from deps_parsing.infrastructure.tl_parsing.excel.line_based_detection import (
    LineBasedDetectionStrategy,
)
from deps_parsing.infrastructure.tl_parsing.table_reference import Point, TableReference


class _ExpectedDetectionResults:
    def __init__(self, sheet_to_tables_mapping: dict[int, list[TableReference]]) -> None:
        self.sheet_to_tables_mapping = sheet_to_tables_mapping

    def assert_correct_tables_detected_for(self, sheet_idx: int, tables: list[TableReference]) -> None:
        expected_tables = self.sheet_to_tables_mapping[sheet_idx]

        assert len(tables) == len(expected_tables)
        for table in tables:
            assert table in expected_tables


@pytest.mark.parametrize(
    "excel_file_path,expected_for_each_sheet",
    [
        (
            "tests/data/excel/1-sheet-with-merged-rows-case.xlsx",
            _ExpectedDetectionResults(
                {
                    0: [
                        TableReference(placement=(Point(row=1, column=0), Point(row=44, column=3))),
                        TableReference(placement=(Point(row=1, column=5), Point(row=44, column=13))),
                    ],
                },
            ),
        ),
        (
            "tests/data/excel/2-sheets-whole-sheet-as-table.xlsx",
            _ExpectedDetectionResults(
                {
                    0: [
                        TableReference(placement=(Point(row=0, column=0), Point(row=116, column=19))),
                    ],
                    1: [
                        TableReference(placement=(Point(row=0, column=0), Point(row=49, column=19))),
                        TableReference(placement=(Point(row=51, column=0), Point(row=116, column=19))),
                    ],
                },
            ),
        ),
        (
            "tests/data/excel/3-sheets-some-basic-cases.xlsx",
            _ExpectedDetectionResults(
                {
                    0: [
                        TableReference(placement=(Point(row=0, column=0), Point(row=67, column=3))),
                    ],
                    1: [
                        TableReference(placement=(Point(row=0, column=0), Point(row=105, column=3))),
                    ],
                    2: [
                        TableReference(placement=(Point(row=0, column=0), Point(row=75, column=3))),
                    ],
                },
            ),
        ),
        (
            "tests/data/excel/6-sheets-different-tables.xlsx",
            _ExpectedDetectionResults(
                {
                    0: [
                        TableReference(placement=(Point(row=0, column=1), Point(row=16, column=3))),
                        TableReference(placement=(Point(row=18, column=1), Point(row=42, column=2))),
                        TableReference(placement=(Point(row=1, column=5), Point(row=7, column=7))),
                        TableReference(placement=(Point(row=18, column=5), Point(row=54, column=7))),
                        TableReference(placement=(Point(row=18, column=10), Point(row=21, column=17))),
                    ],
                    1: [
                        TableReference(placement=(Point(row=1, column=1), Point(row=16, column=3))),
                        TableReference(placement=(Point(row=18, column=1), Point(row=42, column=2))),
                        TableReference(placement=(Point(row=44, column=1), Point(row=65, column=3))),
                        TableReference(placement=(Point(row=1, column=5), Point(row=42, column=12))),
                    ],
                    2: [
                        TableReference(placement=(Point(row=0, column=1), Point(row=13, column=4))),
                        TableReference(placement=(Point(row=15, column=1), Point(row=27, column=3))),
                        TableReference(placement=(Point(row=29, column=2), Point(row=41, column=2))),
                    ],
                    3: [
                        TableReference(placement=(Point(row=1, column=1), Point(row=23, column=13))),
                    ],
                    4: [
                        TableReference(placement=(Point(row=1, column=1), Point(row=21, column=3))),
                        TableReference(placement=(Point(row=1, column=6), Point(row=1, column=6))),
                        TableReference(placement=(Point(row=14, column=6), Point(row=17, column=14))),
                        TableReference(placement=(Point(row=23, column=6), Point(row=30, column=7))),
                    ],
                    5: [
                        TableReference(placement=(Point(row=4, column=1), Point(row=19, column=1))),
                        TableReference(placement=(Point(row=23, column=3), Point(row=40, column=4))),
                        TableReference(placement=(Point(row=3, column=3), Point(row=8, column=14))),
                        TableReference(placement=(Point(row=11, column=3), Point(row=19, column=16))),
                    ],
                },
            ),
        ),
    ],
)
def test_tables_detection(excel_file_path: str, expected_for_each_sheet: _ExpectedDetectionResults) -> None:
    workbook = xl.load_workbook(excel_file_path)
    strategy = LineBasedDetectionStrategy()

    for sheet_idx, sheet in enumerate(workbook):
        result = strategy.detect_tables(sheet)

        expected_for_each_sheet.assert_correct_tables_detected_for(sheet_idx, result)
