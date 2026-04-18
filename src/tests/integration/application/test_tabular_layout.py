import pytest
from deps_tabular_layout.models.events import TabularLayoutDeleted

from deps_parsing.domain.dtos import TabularLayoutFilter
from deps_parsing.domain.exceptions import TabularLayoutNotFound
from tests.factories.tabular_layout import SheetFactory, TabularLayoutFactory


def test_find_tabular_layout__simple_tl__ok(saved_test_tabular_layout, tabular_layout_service):
    tl = tabular_layout_service.find_tabular_layout(
        saved_test_tabular_layout.id(),
        saved_test_tabular_layout.tenant_id(),
        filtering=TabularLayoutFilter(),
    )

    assert tl


def test_find_tabular_layout__with_sheets__ok(
    tabular_layout_command_repository,
    tabular_layout_service,
):
    tl = TabularLayoutFactory.create()
    tabular_layout_command_repository.save(tl)

    founded_tl = tabular_layout_service.find_tabular_layout(
        tl.id(),
        tl.tenant_id(),
        filtering=TabularLayoutFilter(),
    )

    assert founded_tl


def test_find_tabular_layout__with_tables__ok(
    tabular_layout_command_repository,
    tabular_layout_service,
):
    tl = TabularLayoutFactory.create(sheets=[SheetFactory.create(images=[])])
    tabular_layout_command_repository.save(tl)

    founded_tl = tabular_layout_service.find_tabular_layout(
        tl.id(),
        tl.tenant_id(),
        filtering=TabularLayoutFilter,
    )

    assert founded_tl


def test_find_tabular_layout__not_exist__error(
    tabular_layout_service,
):
    with pytest.raises(TabularLayoutNotFound):
        tabular_layout_service.find_tabular_layout("fake_id", "fake_tenant", TabularLayoutFilter())


def test_delete_tabular_layout__ok(
    fake_domain_event_publisher,
    test_saved_tl_with_ordered_cells,
    tabular_layout_service,
    tabular_layout_query_repository,
):
    tabular_layout_service.delete_layout(
        test_saved_tl_with_ordered_cells.id(), test_saved_tl_with_ordered_cells.tenant_id()
    )

    assert (
        tabular_layout_query_repository.is_layout_exists(
            test_saved_tl_with_ordered_cells.id(),
            test_saved_tl_with_ordered_cells.tenant_id(),
        )
        is False
    )
    assert fake_domain_event_publisher.last_published.events[0].id == test_saved_tl_with_ordered_cells.id()
    assert isinstance(fake_domain_event_publisher.last_published.events[0], TabularLayoutDeleted)


def test_delete_tabular_layout__tl_doesnt_exist__no_errors(
    fake_domain_event_publisher,
    test_saved_tl_with_ordered_cells,
    tabular_layout_service,
):
    tabular_layout_service.delete_layout("fake_id", test_saved_tl_with_ordered_cells.tenant_id())

    assert fake_domain_event_publisher.last_published is None


def test_delete_tabular_layout__cells__ok(
    test_saved_tl_with_ordered_cells,
    tabular_layout_service,
    tl_query_helper,
):
    tabular_layout_service.delete_layout_cells(test_saved_tl_with_ordered_cells.id())

    all_cells = tl_query_helper.load_all_cells()

    assert not all_cells
