import openpyxl as xl
import pytest

from deps_parsing.infrastructure.tl_parsing import CSVParser, ExcelParser


@pytest.fixture
def excel_file_path__all_styles() -> str:
    return "tests/data/excel/1-sheet-all-styles.xlsx"


@pytest.fixture
def excel_file_path__large_table() -> str:
    return "tests/data/excel/1-sheet-large-table.xlsx"


@pytest.fixture
def excel_file_bytes__all_styles(excel_file_path__all_styles: str) -> bytes:
    with open(excel_file_path__all_styles, "rb") as file:
        return file.read()


@pytest.fixture
def excel_file_bytes__large_table(excel_file_path__large_table: str) -> bytes:
    with open(excel_file_path__large_table, "rb") as file:
        return file.read()


@pytest.fixture
def excel_file__all_styles(excel_file_path__all_styles: str) -> xl.Workbook:
    return xl.load_workbook(excel_file_path__all_styles)


@pytest.fixture
def cell_all_styles(excel_file__all_styles) -> xl.cell.cell.Cell:
    return excel_file__all_styles["tables"]["A1"]


@pytest.fixture
def merged_cell__root(excel_file__all_styles) -> xl.cell.cell.Cell:
    return excel_file__all_styles["tables"]["C11"]


@pytest.fixture
def merged_cell__sub_cell(excel_file__all_styles) -> xl.cell.cell.Cell:
    return excel_file__all_styles["tables"]["C12"]


@pytest.fixture
def cell_with_hyperlink(excel_file__all_styles) -> xl.cell.cell.Cell:
    return excel_file__all_styles["tables"]["B13"]


@pytest.fixture
def cell_with_comment(excel_file__all_styles) -> xl.cell.cell.Cell:
    return excel_file__all_styles["tables"]["B6"]


@pytest.fixture
def cell_without_comment(excel_file__all_styles) -> xl.cell.cell.Cell:
    return excel_file__all_styles["tables"]["A1"]


@pytest.fixture
def cell_with_all_borders(excel_file__all_styles) -> xl.cell.cell.Cell:
    return excel_file__all_styles["tables"]["C2"]


@pytest.fixture
def cell_with_formula(excel_file__all_styles) -> xl.cell.cell.Cell:
    return excel_file__all_styles["tables"]["A13"]


@pytest.fixture
def table_builder_mock():
    class _TableBuilderMock:
        @property
        def min_column(self) -> int:
            return 0

        @property
        def min_row(self) -> int:
            return 0

    return _TableBuilderMock()


@pytest.fixture
def excel_parser_with_fakes(fake_cell_command_repository, fake_document_proxy):
    return ExcelParser(
        cell_command_repository=fake_cell_command_repository,
        documents_proxy=fake_document_proxy,
    )


@pytest.fixture
def excel_parser_with_mocked_repo(cell_command_repository_mock, fake_document_proxy):
    return ExcelParser(
        cell_command_repository=cell_command_repository_mock,
        documents_proxy=fake_document_proxy,
    )


@pytest.fixture
def csv_parser_with_fakes(fake_cell_command_repository, fake_document_proxy):
    return CSVParser(
        cell_command_repository=fake_cell_command_repository,
        documents_proxy=fake_document_proxy,
    )


@pytest.fixture
def csv_parser_with_mocked_repo(cell_command_repository_mock, fake_document_proxy):
    return CSVParser(
        cell_command_repository=cell_command_repository_mock,
        documents_proxy=fake_document_proxy,
    )


@pytest.fixture(
    params=[
        ("base.csv", 12, 3, 4),
        ("with_breaks.csv", 9, 3, 3),
        ("with_missing_fields.csv", 12, 3, 4),
        ("with_different_delimeters.csv", 12, 4, 3),
        ("with_quotes.csv", 9, 3, 3),
        ("with_trailing_spaces.csv", 9, 3, 3),
        ("with_special_symbols.csv", 9, 3, 3),
    ]
)
def test_csv_data(request):
    file_name, cell_count, cols, rows = request.param
    with open(f"./tests/data/csv/{file_name}", "rb") as f:
        return (f.read(), cell_count, cols, rows)


@pytest.fixture
def test_base_csv_file():
    with open("./tests/data/csv/base.csv", "rb") as f:
        return f.read()


@pytest.fixture
def test_empty_csv_data():
    with open("./tests/data/csv/empty.csv", "rb") as f:
        return f.read()
