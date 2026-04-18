import pytest
from deps_tabular_layout.models import Table, TabularLayout

from deps_parsing.domain.interfaces import ITabularLayoutCommandRepository
from tests.factories.tabular_layout import SheetFactory, TabularLayoutFactory

from ....helper import TLQueryHelper


def test_tl_saving__without_tables__tl_saved(
    tabular_layout_command_repository: ITabularLayoutCommandRepository,
    tl_query_helper: TLQueryHelper,
):
    layout = TabularLayoutFactory.create(
        sheets=[SheetFactory(tables=[]) for _ in range(3)],
    )

    tabular_layout_command_repository.save(layout)

    saved_layouts = tl_query_helper.load_all_tabular_layouts()
    assert saved_layouts
    assert len(saved_layouts) == 1

    _assert_tl_equal_raw_tl(layout, saved_layouts[0])

    saved_tables = tl_query_helper.load_all_tables()
    assert not saved_tables


def test_tl_saving__tl_saved__tables_saved(
    tabular_layout_command_repository: ITabularLayoutCommandRepository,
    tl_query_helper: TLQueryHelper,
):
    layout = TabularLayoutFactory.create()

    tabular_layout_command_repository.save(layout)

    saved_layouts = tl_query_helper.load_all_tabular_layouts()
    assert saved_layouts
    assert len(saved_layouts) == 1

    _assert_tl_equal_raw_tl(layout, saved_layouts[0])

    saved_tables = tl_query_helper.load_all_tables()
    for table, saved_table in zip(layout.iter_tables(), saved_tables):
        _assert_table_equal_raw_table(table, saved_table)


def test_tl_saving__existing_tl__tl_updated__tables_replaced(
    tabular_layout_command_repository: ITabularLayoutCommandRepository,
    tl_query_helper: TLQueryHelper,
):
    layout: TabularLayout = TabularLayoutFactory.create()
    tabular_layout_command_repository.save(layout)

    updated_layout: TabularLayout = TabularLayoutFactory.create(
        id_=layout.id,
        tenant_id=layout.tenant_id,
    )
    tabular_layout_command_repository.save(updated_layout)

    saved_layouts = tl_query_helper.load_all_tabular_layouts()
    assert len(saved_layouts) == 1
    _assert_tl_equal_raw_tl(updated_layout, saved_layouts[0])

    saved_tables = tl_query_helper.load_all_tables()
    assert len(saved_tables) == len(list(updated_layout.iter_tables()))
    for table, saved_table in zip(updated_layout.iter_tables(), saved_tables):
        _assert_table_equal_raw_table(table, saved_table)


def test_deleting_tl__tl_deleted__tables_deleted(
    tabular_layout_command_repository: ITabularLayoutCommandRepository,
    tl_query_helper: TLQueryHelper,
):
    layout: TabularLayout = TabularLayoutFactory.create()
    tabular_layout_command_repository.save(layout)

    layouts = tl_query_helper.load_all_tabular_layouts()
    tables = tl_query_helper.load_all_tables()

    assert len(layouts) == 1
    assert len(tables) == len(list(layout.iter_tables()))

    tabular_layout_command_repository.delete(layout_id=layout.id(), tenant_id=layout.tenant_id())

    layouts = tl_query_helper.load_all_tabular_layouts()
    tables = tl_query_helper.load_all_tables()

    assert len(layouts) == 0
    assert len(tables) == 0


def test_deleting_tl__other_tenant__nothing_deleted(
    tabular_layout_command_repository: ITabularLayoutCommandRepository,
    tl_query_helper: TLQueryHelper,
):
    layout: TabularLayout = TabularLayoutFactory.create()
    tabular_layout_command_repository.save(layout)
    tabular_layout_command_repository.delete(layout_id=layout.id(), tenant_id="fake_tenant")

    layouts = tl_query_helper.load_all_tabular_layouts()
    tables = tl_query_helper.load_all_tables()

    assert len(layouts) == 1
    assert len(tables) == len(list(layout.iter_tables()))


def test_deleting_tl__other_id__no_errors(
    tabular_layout_command_repository: ITabularLayoutCommandRepository,
    tl_query_helper: TLQueryHelper,
):
    layout: TabularLayout = TabularLayoutFactory.create()
    tabular_layout_command_repository.save(layout)
    tabular_layout_command_repository.delete(layout_id="fake_id", tenant_id=layout.tenant_id())

    layouts = tl_query_helper.load_all_tabular_layouts()
    tables = tl_query_helper.load_all_tables()

    assert len(layouts) == 1
    assert len(tables) == len(list(layout.iter_tables()))


def _assert_tl_equal_raw_tl(layout: TabularLayout, raw_layout: dict) -> None:
    assert layout.id() == raw_layout["id"]
    assert layout.tenant_id() == raw_layout["tenant_id"]
    assert layout.parsing_type == raw_layout["parsing_type"]
    assert layout.extracted_properties == raw_layout["extracted_properties"]

    assert len(layout.sheets) == len(raw_layout["sheets"])

    for sheet, raw_sheet in zip(layout.sheets, raw_layout["sheets"]):
        assert sheet.id() == raw_sheet["id"]
        assert sheet.title == raw_sheet["title"]
        assert sheet.is_hidden == raw_sheet["is_hidden"]

        assert len(sheet.tables) == len(raw_sheet["table_ids"])
        for table in sheet.tables:
            assert table.id() in raw_sheet["table_ids"]

        assert len(sheet.images) == len(raw_sheet["images"])
        for image, raw_image in zip(sheet.images, raw_sheet["images"]):
            assert image.id() == raw_image["id"]
            assert image.file_path == raw_image["file_path"]
            assert image.type == raw_image["type"]
            assert image.title == raw_image["title"]
            assert image.description == raw_image["description"]


def _assert_table_equal_raw_table(table: Table, raw_table: dict) -> None:
    assert table.id() == raw_table["id"]
    assert table.sheet_id() == raw_table["sheet_id"]
    assert table.row_count == raw_table["row_count"]
    assert table.column_count == raw_table["column_count"]
