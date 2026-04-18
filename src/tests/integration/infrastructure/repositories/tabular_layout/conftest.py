import pytest

from tests.factories.tabular_layout import SheetFactory, TabularLayoutFactory


@pytest.fixture
def test_saved_tl_without_tables_and_images(tabular_layout_command_repository):
    tl = TabularLayoutFactory.create(sheets=[SheetFactory.create(tables=[], images=[])])
    tabular_layout_command_repository.save(tl)
    return tl


@pytest.fixture
def test_saved_tl_without_sheets(tabular_layout_command_repository):
    tl = TabularLayoutFactory.create(sheets=[])
    tabular_layout_command_repository.save(tl)
    return tl
