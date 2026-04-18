import pytest
from deps_tabular_layout.models import Cell, EntityId, Point
from sqlalchemy.exc import IntegrityError

from deps_parsing.domain.interfaces import ICellCommandRepository
from tests.factories.tabular_layout import CellFactory, StyleFactory

from ....helper import TLQueryHelper


def test_cell_saving__without_attributes(
    document_layout_id,
    cell_command_repository: ICellCommandRepository,
    tl_query_helper: TLQueryHelper,
):
    cell_wo_properties = CellFactory.create(
        merge=None,
        style=None,
        comment=None,
        alignment=None,
        borders=None,
    )

    cell_command_repository.save_batch(document_layout_id, [cell_wo_properties])

    saved_cells = tl_query_helper.load_all_cells()

    assert saved_cells
    assert len(saved_cells) == 1
    _assert_cell_equal_raw_cell(cell_wo_properties, saved_cells[0])


def test_cell_saving__multiple_cells_saved(
    document_layout_id,
    cell_command_repository: ICellCommandRepository,
    tl_query_helper: TLQueryHelper,
):
    cells = CellFactory.create_batch(5)

    cell_command_repository.save_batch(document_layout_id, cells)

    saved_cells = tl_query_helper.load_all_cells()

    assert saved_cells
    assert len(saved_cells) == 5

    for cell, saved_cell in zip(cells, saved_cells):
        _assert_cell_equal_raw_cell(cell, saved_cell)


def test_cell_saving__existing_cells_ignored_new_added(
    document_layout_id,
    cell_command_repository: ICellCommandRepository,
    tl_query_helper: TLQueryHelper,
):
    first_batch = CellFactory.create_batch(5)
    cell_command_repository.save_batch(document_layout_id, first_batch)

    second_batch = CellFactory.create_batch(5)
    extended_cells = first_batch + second_batch
    cell_command_repository.save_batch(document_layout_id, extended_cells)

    saved_cells = tl_query_helper.load_all_cells()
    assert len(saved_cells) == 10


def test_cell_updation__property_added_later(
    document_layout_id,
    cell_command_repository: ICellCommandRepository,
    tl_query_helper: TLQueryHelper,
):
    cell = CellFactory.create(style=None)
    cell_command_repository.save_batch(document_layout_id, [cell])
    saved_cell = tl_query_helper.load_all_cells()[0]
    assert saved_cell["style"] is None

    cell.style = StyleFactory.create()
    cell_command_repository.save_batch(document_layout_id, [cell])
    saved_cell = tl_query_helper.load_all_cells()[0]
    assert saved_cell["style"] is not None


def test_cell_creation__same_table_same_relatives_coordinates__error(
    document_layout_id,
    cell_command_repository: ICellCommandRepository,
):
    cell_1 = CellFactory.create(relative_position=Point(x=0, y=0), table_id=EntityId("1"))
    cell_2 = CellFactory.create(relative_position=Point(x=0, y=0), table_id=EntityId("1"))

    cell_command_repository.save_batch(document_layout_id, [cell_1])

    with pytest.raises(IntegrityError):
        cell_command_repository.save_batch(document_layout_id, [cell_2])


def test_cell_creation__different_tables_same_relatives_coordinates__success(
    document_layout_id,
    cell_command_repository: ICellCommandRepository,
):
    cell_1 = CellFactory.create(relative_position=Point(x=0, y=0), table_id=EntityId("1"))
    cell_2 = CellFactory.create(relative_position=Point(x=0, y=0), table_id=EntityId("2"))

    cell_command_repository.save_batch(document_layout_id, [cell_1])
    cell_command_repository.save_batch(document_layout_id, [cell_2])


def test_deleting_cells_of_layout__deleted(
    document_id: str,
    cell_command_repository: ICellCommandRepository,
    tl_query_helper: TLQueryHelper,
):
    batch_size = 5
    first_batch = CellFactory.create_batch(size=batch_size)
    cell_command_repository.save_batch(layout_id=document_id, cells=first_batch)
    second_batch = CellFactory.create_batch(size=batch_size)
    cell_command_repository.save_batch(layout_id=document_id, cells=second_batch)

    cells = tl_query_helper.load_all_cells()

    assert len(cells) == batch_size * 2

    cell_command_repository.delete(document_id)
    cells = tl_query_helper.load_all_cells()

    assert not cells


def test_deleting_cells_of_layout__fake_layout__no_errors(
    document_id: str,
    cell_command_repository: ICellCommandRepository,
    tl_query_helper: TLQueryHelper,
):
    batch_size = 5
    first_batch = CellFactory.create_batch(size=batch_size)
    cell_command_repository.save_batch(layout_id=document_id, cells=first_batch)

    cell_command_repository.delete("fake_id")
    cells = tl_query_helper.load_all_cells()

    assert len(cells) == batch_size


def _assert_cell_equal_raw_cell(cell: Cell, raw_cell: dict) -> None:
    assert cell.id() == raw_cell["id"]
    assert cell.table_id() == raw_cell["table_id"]
    assert cell.content == raw_cell["content"]
    assert cell.data_type == raw_cell["data_type"]
    assert cell.relative_position.x == raw_cell["relative_position_column"]
    assert cell.relative_position.y == raw_cell["relative_position_row"]
    assert cell.absolute_position.x == raw_cell["absolute_position_column"]
    assert cell.absolute_position.y == raw_cell["absolute_position_row"]
    assert raw_cell["tabular_layout_id"]

    if cell.merge is not None:
        assert cell.merge.column_span == raw_cell["merge"]["column_span"]
        assert cell.merge.row_span == raw_cell["merge"]["row_span"]

    if cell.style is not None:
        assert cell.style.font_name == raw_cell["style"]["font_name"]
        assert cell.style.font_size == raw_cell["style"]["font_size"]
        assert cell.style.color == raw_cell["style"]["color"]
        assert cell.style.background_color == raw_cell["style"]["background_color"]
        assert cell.style.hyperlink == raw_cell["style"]["hyperlink"]
        assert cell.style.bold == raw_cell["style"]["bold"]
        assert cell.style.italic == raw_cell["style"]["italic"]
        assert cell.style.underlined == raw_cell["style"]["underlined"]
        assert cell.style.strikethrough == raw_cell["style"]["strikethrough"]

    if cell.comment is not None:
        assert cell.comment.content == raw_cell["comment"]["content"]
        assert cell.comment.author == raw_cell["comment"]["author"]

    if cell.alignment is not None:
        assert cell.alignment.horizontal == raw_cell["alignment"]["horizontal"]
        assert cell.alignment.vertical == raw_cell["alignment"]["vertical"]

    if cell.borders is not None:
        assert cell.borders.top == raw_cell["borders"]["top"]
        assert cell.borders.bottom == raw_cell["borders"]["bottom"]
        assert cell.borders.left == raw_cell["borders"]["left"]
        assert cell.borders.right == raw_cell["borders"]["right"]
