from itertools import chain

import pytest

from deps_parsing.domain.dtos import TabularLayoutFilter


def test_get_tl_projection__ok(
    test_saved_tl_with_ordered_cells,
    tabular_layout_query_repository,
):
    result = tabular_layout_query_repository.layout_projection_of_id(
        test_saved_tl_with_ordered_cells.id(),
        tenant_id=test_saved_tl_with_ordered_cells.tenant_id(),
        filtering=TabularLayoutFilter(),
    )

    assert result.id == test_saved_tl_with_ordered_cells.id()
    assert result.tenant_id == test_saved_tl_with_ordered_cells.tenant_id()
    assert result.parsing_type == test_saved_tl_with_ordered_cells.parsing_type
    assert result.extracted_properties == test_saved_tl_with_ordered_cells.extracted_properties
    assert len(result.sheets) == len(test_saved_tl_with_ordered_cells.sheets)
    assert len(result.tables) == sum((len(sheet.tables) for sheet in test_saved_tl_with_ordered_cells.sheets))


@pytest.mark.parametrize("fixture_name", ["test_saved_tl_without_sheets", "test_saved_tl_without_tables_and_images"])
def test_get_tl_projection__not_full_tl__no_error(fixture_name, request, tabular_layout_query_repository):
    layout = request.getfixturevalue(fixture_name)
    result = tabular_layout_query_repository.layout_projection_of_id(
        layout_id=layout.id(),
        tenant_id=layout.tenant_id(),
        filtering=TabularLayoutFilter(),
    )

    assert result


def test_get_tl_projection__sheets_data__are_correct(
    test_saved_tl_with_ordered_cells,
    tabular_layout_query_repository,
):
    result = tabular_layout_query_repository.layout_projection_of_id(
        test_saved_tl_with_ordered_cells.id(),
        tenant_id=test_saved_tl_with_ordered_cells.tenant_id(),
        filtering=TabularLayoutFilter(),
    )

    for sheet, compared_sheet in zip(
        sorted(test_saved_tl_with_ordered_cells.sheets, key=lambda item: item.id()),
        sorted(result.sheets, key=lambda item: item.id),
    ):
        assert sheet.id() == compared_sheet.id
        assert sheet.title == compared_sheet.title
        assert sheet.is_hidden == compared_sheet.is_hidden
        assert [table.id() for table in sheet.tables] == compared_sheet.table_ids
        for orig_image, restored_image in zip(
            sorted(sheet.images, key=lambda item: item.id()),
            sorted(compared_sheet.images, key=lambda item: item.id()),
        ):
            assert orig_image == restored_image


def test_get_tl_projection__tables_data__are_correct(
    test_saved_tl_with_ordered_cells,
    tabular_layout_query_repository,
):
    result = tabular_layout_query_repository.layout_projection_of_id(
        test_saved_tl_with_ordered_cells.id(),
        tenant_id=test_saved_tl_with_ordered_cells.tenant_id(),
        filtering=TabularLayoutFilter(),
    )
    for table, restored_table in zip(
        sorted((table for table in test_saved_tl_with_ordered_cells.iter_tables()), key=lambda item: item.id()),
        sorted((table.schema for table in result.tables), key=lambda item: item.id),
    ):
        assert table.id() == restored_table.id
        assert table.sheet_id() == restored_table.sheet_id
        assert table.column_count == restored_table.column_count
        assert table.row_count == restored_table.row_count
        assert table.placement == restored_table.placement


def test_get_tl_projection__cells_data__are_correct(
    test_saved_tl_with_ordered_cells,
    test_saved_ordered_cells,
    tabular_layout_query_repository,
):
    result = tabular_layout_query_repository.layout_projection_of_id(
        test_saved_tl_with_ordered_cells.id(),
        tenant_id=test_saved_tl_with_ordered_cells.tenant_id(),
        filtering=TabularLayoutFilter(),
    )
    for cell, restored_cell in zip(
        sorted(test_saved_ordered_cells, key=lambda item: item.id()),
        sorted(chain(cell_lst for table in result.tables for cell_lst in table.data), key=lambda item: item.id()),
    ):
        assert cell.id() == restored_cell.id()
        assert cell.table_id() == restored_cell.table_id()
        assert cell.absolute_position == restored_cell.absolute_position
        assert cell.alignment == restored_cell.alignment
        assert cell.borders == restored_cell.borders
        assert cell.comment == restored_cell.comment
        assert cell.content == restored_cell.content
        assert cell.data_type == restored_cell.data_type
        assert cell.merge == restored_cell.merge
        assert cell.relative_position == restored_cell.relative_position
        assert cell.style == restored_cell.style


def test_get_tl_projection__with_table_filtering__ok(
    tabular_layout_query_repository,
    test_saved_tl_with_ordered_cells,
):
    needed_table_ids = [sheet.tables[-1].id() for sheet in test_saved_tl_with_ordered_cells.sheets]
    result = tabular_layout_query_repository.layout_projection_of_id(
        layout_id=test_saved_tl_with_ordered_cells.id(),
        tenant_id=test_saved_tl_with_ordered_cells.tenant_id(),
        filtering=TabularLayoutFilter(tables=needed_table_ids),
    )

    assert len(result.tables) == len(needed_table_ids)
    assert {table.schema.id for table in result.tables} == set(needed_table_ids)


def test_get_tl_projection__with_row_filtering__ok(
    tabular_layout_query_repository,
    test_saved_tl_with_ordered_cells,
):
    result = tabular_layout_query_repository.layout_projection_of_id(
        layout_id=test_saved_tl_with_ordered_cells.id(),
        tenant_id=test_saved_tl_with_ordered_cells.tenant_id(),
        filtering=TabularLayoutFilter(row_span=(1, 2)),
    )

    assert {cell.relative_position.y for table in result.tables for cell in table.data} == {1, 2}


def test_get_tl_projection__with_col_filtering__ok(
    tabular_layout_query_repository,
    test_saved_tl_with_ordered_cells,
):
    result = tabular_layout_query_repository.layout_projection_of_id(
        layout_id=test_saved_tl_with_ordered_cells.id(),
        tenant_id=test_saved_tl_with_ordered_cells.tenant_id(),
        filtering=TabularLayoutFilter(col_span=(1, 1)),
    )

    assert {cell.relative_position.x for table in result.tables for cell in table.data} == {1}


def test_get_tl_projection__with_all_filtering__ok(
    tabular_layout_query_repository,
    test_saved_tl_with_ordered_cells,
):
    table_id = test_saved_tl_with_ordered_cells.sheets[0].tables[0].id()
    result = tabular_layout_query_repository.layout_projection_of_id(
        layout_id=test_saved_tl_with_ordered_cells.id(),
        tenant_id=test_saved_tl_with_ordered_cells.tenant_id(),
        filtering=TabularLayoutFilter(
            tables=[table_id],
            col_span=(0, 0),
            row_span=(0, 0),
        ),
    )

    assert len(result.tables) == 1
    assert len(result.tables[0].data) == 1


@pytest.mark.parametrize(
    "filter_name, filter_value", [("tables", "fake_table_id"), ("col_span", (100, 100)), ("row_span", (100, 100))]
)
def test_get_tl_projection__invalid_filter_data__no_tables(
    filter_name, filter_value, tabular_layout_query_repository, test_saved_tl_with_ordered_cells
):
    result = tabular_layout_query_repository.layout_projection_of_id(
        layout_id=test_saved_tl_with_ordered_cells.id(),
        tenant_id=test_saved_tl_with_ordered_cells.tenant_id(),
        filtering=TabularLayoutFilter(
            **{filter_name: filter_value},
        ),
    )

    assert not result.tables


def test_get_tl_projection__invalid_id__none_returns(tabular_layout_query_repository, test_saved_tl_with_ordered_cells):
    result = tabular_layout_query_repository.layout_projection_of_id(
        layout_id="fake_tl_id",
        tenant_id=test_saved_tl_with_ordered_cells.tenant_id(),
        filtering=TabularLayoutFilter(),
    )

    assert not result


def test_get_tl_projection__invalid_tenant_id__none_returns(
    tabular_layout_query_repository, test_saved_tl_with_ordered_cells
):
    result = tabular_layout_query_repository.layout_projection_of_id(
        layout_id=test_saved_tl_with_ordered_cells.id(),
        tenant_id="fake_tenant_id",
        filtering=TabularLayoutFilter(),
    )

    assert not result


def test_get_layout_info__ok(tabular_layout_query_repository, test_saved_tl_with_ordered_cells):
    result = tabular_layout_query_repository.layout_of_id_info(
        test_saved_tl_with_ordered_cells.id(),
        test_saved_tl_with_ordered_cells.tenant_id(),
    )

    assert result.id == test_saved_tl_with_ordered_cells.id()
    assert result.parsing_type == test_saved_tl_with_ordered_cells.parsing_type
    assert len(result.sheets) == len(test_saved_tl_with_ordered_cells.sheets)
    for orig_sheet, compared_sheet in zip(
        sorted(test_saved_tl_with_ordered_cells.sheets, key=lambda item: item.id()),
        sorted(result.sheets, key=lambda item: item.id),
    ):
        assert orig_sheet.id() == compared_sheet.id
        assert orig_sheet.title == compared_sheet.title
        assert orig_sheet.is_hidden == compared_sheet.is_hidden
        assert set(image.id() for image in orig_sheet.images) == set(compared_sheet.images)
        for orig_table, compared_table in zip(
            sorted(orig_sheet.tables, key=lambda item: item.id()),
            sorted(compared_sheet.tables, key=lambda item: item.id),
        ):
            assert orig_table.id() == compared_table.id
            assert orig_table.row_count == compared_table.row_count
            assert orig_table.column_count == compared_table.column_count


@pytest.mark.parametrize("fixture_name", ["test_saved_tl_without_sheets", "test_saved_tl_without_tables_and_images"])
def test_get_layout_info__not_full_tl__no_error(fixture_name, request, tabular_layout_query_repository):
    layout = request.getfixturevalue(fixture_name)
    result = tabular_layout_query_repository.layout_of_id_info(layout.id(), layout.tenant_id())

    assert result


def test_get_layout_info__no_layout__no_errors(
    tabular_layout_query_repository,
    test_saved_tl_with_ordered_cells,
    tenant_id,
):
    result = tabular_layout_query_repository.layout_of_id_info(
        layout_id="fake_id",
        tenant_id=tenant_id,
    )
    assert result is None


def test_get_layout_info__layout_from_other_org__empty_result(
    tabular_layout_query_repository,
    test_saved_tl_with_ordered_cells,
):
    result = tabular_layout_query_repository.layout_of_id_info(
        layout_id=test_saved_tl_with_ordered_cells.id(),
        tenant_id="fake_tenant",
    )
    assert result is None


def test_layout_exists__layout_exists__returns_true(tabular_layout_query_repository, test_saved_tl_without_sheets):
    result = tabular_layout_query_repository.is_layout_exists(
        test_saved_tl_without_sheets.id(),
        test_saved_tl_without_sheets.tenant_id(),
    )

    assert result is True


def test_layout_exists__layout_doesnt_exist__returns_false(
    tabular_layout_query_repository,
    test_saved_tl_without_sheets,
):
    result = tabular_layout_query_repository.is_layout_exists(
        "fake_tl_id",
        test_saved_tl_without_sheets.tenant_id(),
    )

    assert result is False


def test_layout_exists__layout_from_other_tenant__returns_false(
    tabular_layout_query_repository,
    test_saved_tl_without_sheets,
):
    result = tabular_layout_query_repository.is_layout_exists(
        test_saved_tl_without_sheets.id(),
        "fake_tenant",
    )

    assert result is False


def test_get_tl__ok(
    test_saved_tl_with_ordered_cells,
    tabular_layout_query_repository,
):
    result = tabular_layout_query_repository.layout_of_id(
        test_saved_tl_with_ordered_cells.id(),
        tenant_id=test_saved_tl_with_ordered_cells.tenant_id(),
    )

    assert result.id == test_saved_tl_with_ordered_cells.id
    assert result.tenant_id == test_saved_tl_with_ordered_cells.tenant_id
    assert result.parsing_type == test_saved_tl_with_ordered_cells.parsing_type
    assert result.extracted_properties == test_saved_tl_with_ordered_cells.extracted_properties
    assert result.sheets == test_saved_tl_with_ordered_cells.sheets


def test_get_tl__other_tenant__none_returns(
    test_saved_tl_with_ordered_cells,
    tabular_layout_query_repository,
):
    result = tabular_layout_query_repository.layout_of_id(
        layout_id=test_saved_tl_with_ordered_cells.id(),
        tenant_id="fake_tenant",
    )

    assert result is None


def test_get_tl__invalid_id__none_returns(
    test_saved_tl_with_ordered_cells,
    tabular_layout_query_repository,
):
    result = tabular_layout_query_repository.layout_of_id(
        layout_id="fake_layout_id",
        tenant_id=test_saved_tl_with_ordered_cells.id(),
    )

    assert result is None
