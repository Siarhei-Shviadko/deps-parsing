import pytest
from deps_tabular_layout.models import DataType

from deps_parsing.infrastructure.tl_parsing.excel.mappers import (
    CommentMapper,
    DataTypeMapper,
    FormatMapper,
    PositionMapper,
)


def test_comment_mapper__cell_has_comment(cell_with_comment):
    comment_text = cell_with_comment.comment.text
    comment_input = CommentMapper.from_cell(cell_with_comment)

    assert comment_input.author is not None
    assert comment_input.content == comment_text


def test_comment_mapper__cell_has_no_comment(cell_without_comment):
    comment_input = CommentMapper.from_cell(cell_without_comment)

    assert comment_input is None


def test_format_mapper__cell_all_formats(cell_all_styles):
    format_input = FormatMapper.from_cell(cell_all_styles)

    assert format_input.style.bold is True
    assert format_input.style.italic is True
    assert format_input.style.underlined is True
    assert format_input.style.strikethrough is True
    assert format_input.style.color == "FFFF0000"
    assert format_input.style.font_size == "11.0"
    assert format_input.style.font_name == "Calibri Light"

    assert format_input.style.hyperlink is False


def test_borders__all_borders(cell_with_all_borders):
    format_input = FormatMapper.from_cell(cell_with_all_borders)

    assert format_input.borders.top == "thin"
    assert format_input.borders.bottom == "thin"
    assert format_input.borders.left == "thin"
    assert format_input.borders.right == "thin"


def test_hyperlink__cell_has_hyperlink(cell_with_hyperlink):
    format_input = FormatMapper.from_cell(cell_with_hyperlink)

    assert format_input.style.hyperlink is not None


@pytest.mark.parametrize(
    "cell_coordinates,expected_data_type",
    [
        ("A11", DataType.FORMULA),
        ("B18", DataType.NUMERIC),
        ("B7", DataType.STRING),
        ("B22", DataType.BOOL),
    ],
)
def test_data_types(
    excel_file__all_styles,
    cell_coordinates: str,
    expected_data_type: DataType,
):
    cell = excel_file__all_styles["tables"][cell_coordinates]
    data_type = DataTypeMapper.from_cell(cell)

    assert data_type == expected_data_type


def test_position_mapper__cell_position__unmerged_cell(
    cell_all_styles,
    excel_file__all_styles,
    table_builder_mock,
):
    position_input = PositionMapper.from_excel(
        cell=cell_all_styles,
        sheet=excel_file__all_styles["tables"],
        table_builder=table_builder_mock,
    )

    assert position_input.absolute_position == (0, 0)
    assert position_input.relative_position == (0, 0)
    assert position_input.merge is None


def test_position_mapper__cell_position__merged_cell(
    merged_cell__root,
    excel_file__all_styles,
    table_builder_mock,
):
    position_input = PositionMapper.from_excel(
        cell=merged_cell__root,
        sheet=excel_file__all_styles["tables"],
        table_builder=table_builder_mock,
    )

    assert position_input.absolute_position == (2, 10)
    assert position_input.relative_position == (2, 10)
    assert position_input.merge == (2, 2)
