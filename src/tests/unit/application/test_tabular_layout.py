import uuid

import pytest
from deps_tabular_layout.models import ParsingType as TLParsingType
from deps_tabular_layout.models import TabularLayout

from deps_parsing.application import TabularLayoutService
from deps_parsing.domain.interfaces import ITabularLayoutQueryRepository


def test_unsupported_parsing_type__error(tabular_layout_service: TabularLayoutService):
    with pytest.raises(NotImplementedError):
        tabular_layout_service.parse(
            document_id="document_id",
            tenant_id="tenant_id",
            parsing_type=TLParsingType.CUSTOM,
            features=set(),
            language=None,
        )


def test_parse_excel__excel_parsing_service_handled_request(
    empty_tabular_layout,
    mocked_excel_parser,
    tabular_layout_service__with_mocked_excel_parser: TabularLayoutService,
):
    mocked_excel_parser.parse.return_value = empty_tabular_layout

    tabular_layout_service__with_mocked_excel_parser.parse(
        document_id="document_id",
        tenant_id="tenant_id",
        parsing_type=TLParsingType.EXCEL,
        features=set(),
        language=None,
    )

    mocked_excel_parser.parse.assert_called_once()


def test_delete_layout__not_exists__no_error(
    fake_tl_query_repository: ITabularLayoutQueryRepository,
    tabular_layout_service: TabularLayoutService,
):
    tabular_layout_service.delete_layout(layout_id=uuid.uuid4().hex, tenant_id=uuid.uuid4().hex)


def test_delete_layout__exists__deleted(
    tenant_id: str,
    fake_tl_query_repository: ITabularLayoutQueryRepository,
    test_saved_full_tabular_layout: TabularLayout,
    tabular_layout_service: TabularLayoutService,
):
    layout_id = test_saved_full_tabular_layout.id()

    assert fake_tl_query_repository.is_layout_exists(layout_id=layout_id, tenant_id=tenant_id)

    tabular_layout_service.delete_layout(layout_id=layout_id, tenant_id=tenant_id)

    assert not fake_tl_query_repository.is_layout_exists(layout_id=layout_id, tenant_id=tenant_id)
