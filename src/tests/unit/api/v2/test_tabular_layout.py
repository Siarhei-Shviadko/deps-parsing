from http import HTTPStatus

from deps_parsing.constants import V2_API_PREFIX
from deps_parsing.domain.dtos import TabularLayoutFilter
from deps_parsing.domain.exceptions import TabularLayoutNotFound
from tests.data.tabular_layout import tabular_layout_projection


def test_get_tabular_layout__no_layout__404_error(client, tabular_layout_service_mock, tenant_id):
    tl_id = "fake_tl_id"
    tabular_layout_service_mock.find_tabular_layout.side_effect = TabularLayoutNotFound(tl_id)

    response = client.get(
        f"{V2_API_PREFIX}/tabular-layout/{tl_id}",
    )

    assert response.status_code == HTTPStatus.NOT_FOUND

    tabular_layout_service_mock.find_tabular_layout.assert_called_with(
        layout_id=tl_id,
        tenant_id=tenant_id,
        filtering=TabularLayoutFilter(
            tables=None,
            row_span=None,
            col_span=None,
        ),
    )


def test_get_tabular_layout__ok(client, tabular_layout_service_mock, tenant_id):
    tabular_layout_projection.tenant_id = tenant_id
    tabular_layout_service_mock.find_tabular_layout.return_value = tabular_layout_projection

    response = client.get(
        f"{V2_API_PREFIX}/tabular-layout/{tabular_layout_projection.id}",
    )
    assert response.status_code == HTTPStatus.OK

    tabular_layout_service_mock.find_tabular_layout.assert_called_with(
        layout_id=tabular_layout_projection.id,
        tenant_id=tabular_layout_projection.tenant_id,
        filtering=TabularLayoutFilter(tables=None, row_span=None, col_span=None),
    )


def test_get_tabular_layout__with_filtering__filter_passed(client, tabular_layout_service_mock, tenant_id):
    tabular_layout_projection.tenant_id = tenant_id
    tabular_layout_service_mock.find_tabular_layout.return_value = tabular_layout_projection

    response = client.get(
        f"{V2_API_PREFIX}/tabular-layout/{tabular_layout_projection.id}",
        params={"tables": ["1", "2"], "rowSpan": [1, 2], "colSpan": [1, 3]},
    )
    assert response.status_code == HTTPStatus.OK
    tabular_layout_service_mock.find_tabular_layout.assert_called_with(
        layout_id=tabular_layout_projection.id,
        tenant_id=tabular_layout_projection.tenant_id,
        filtering=TabularLayoutFilter(tables=["1", "2"], row_span=(1, 2), col_span=(1, 3)),
    )
