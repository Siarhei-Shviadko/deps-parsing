import pytest
from deps_document_layout.model import EntityId
from deps_document_layout.model import ParsingType as DLParsingType
from deps_tabular_layout.models import ParsingType as TLParsingType

from deps_parsing.domain.exceptions import UnsupportedParsingType


def test_parsing_service__page_based_doc__goes_to_dl_service(
    document_mock,
    document_layout_service_mock,
    tabular_layout_service_mock,
    parsing_service,
    document_id,
    tenant_id,
):
    document_mock.get_brief_document_info.return_value = {
        "id": document_id,
        "title": "55130487",
        "state": "completed",
        "files": ["9af4d1792c2e42fab1be636a46aec200.docx"],
        "typeId": "899948a1a50a4a059fd56863dd64dcdc",
        "engine": None,
        "language": None,
        "llmType": "dial@openai.gpt-3.5-turbo",
        "errorInState": None,
        "metadata": None,
    }
    document_layout_service_mock.parse.return_value = EntityId()

    dl_id = parsing_service.perform_parsing(
        document_id=document_id,
        tenant_id=tenant_id,
        features={},
    )

    assert dl_id
    tabular_layout_service_mock.parse.assert_not_called()
    assert document_layout_service_mock.parse.call_count == 1
    document_layout_service_mock.parse.assert_called_once_with(
        document_id=document_id,
        tenant_id=tenant_id,
        parsing_type=DLParsingType("DOCX"),
        features={},
        language=None,
    )


def test_parsing_service__tabular_based_doc__goes_to_tl_service(
    document_mock,
    document_layout_service_mock,
    tabular_layout_service_mock,
    parsing_service,
    document_id,
    tenant_id,
):
    document_mock.get_brief_document_info.return_value = {
        "id": document_id,
        "title": "55130487",
        "state": "completed",
        "files": ["9af4d1792c2e42fab1be636a46aec200.csv"],
        "typeId": "899948a1a50a4a059fd56863dd64dcdc",
        "engine": None,
        "language": None,
        "llmType": "dial@openai.gpt-3.5-turbo",
        "errorInState": None,
        "metadata": None,
    }
    tabular_layout_service_mock.parse.return_value = EntityId()

    dl_id = parsing_service.perform_parsing(
        document_id=document_id,
        tenant_id=tenant_id,
        features={},
    )

    assert dl_id
    document_layout_service_mock.parse.assert_not_called()
    assert tabular_layout_service_mock.parse.call_count == 1
    tabular_layout_service_mock.parse.assert_called_once_with(
        document_id=document_id,
        parsing_type=TLParsingType("CSV"),
        features={},
        language=None,
        tenant_id=tenant_id,
    )


def test_parsing_service__determine_parsing_type_by_engine__ok(
    document_mock,
    document_layout_service_mock,
    tabular_layout_service_mock,
    parsing_service,
    document_id,
    tenant_id,
):
    document_mock.get_brief_document_info.return_value = {
        "id": document_id,
        "title": "55130487",
        "state": "completed",
        "files": ["9af4d1792c2e42fab1be636a46aec200.png"],
        "typeId": "899948a1a50a4a059fd56863dd64dcdc",
        "engine": "TESSERACT",
        "language": None,
        "llmType": "dial@openai.gpt-3.5-turbo",
        "errorInState": None,
        "metadata": None,
    }
    document_layout_service_mock.parse.return_value = EntityId()

    dl_id = parsing_service.perform_parsing(
        document_id=document_id,
        tenant_id=tenant_id,
        engine="TESSERACT",
        features={},
    )

    assert dl_id
    tabular_layout_service_mock.parse.assert_not_called()
    assert document_layout_service_mock.parse.call_count == 1
    document_layout_service_mock.parse.assert_called_once_with(
        document_id=document_id,
        parsing_type=DLParsingType("TESSERACT"),
        features={},
        language=None,
        tenant_id=tenant_id,
    )


def test_parsing_service__doc_with_command_channel__goes_to_plugin(
    document_type_repository_mock,
    fake_command_producer,
    parsing_service,
    document_id,
    tenant_id,
    test_document_type,
):
    document_type_repository_mock.find_by_id_for_tenant.return_value = test_document_type
    parsing_service.perform_parsing(
        document_id=document_id,
        tenant_id=tenant_id,
        document_type_id=test_document_type.id(),
        features={},
    )

    assert fake_command_producer.last_sended
    assert fake_command_producer.last_sended.command.document_id == document_id
    assert fake_command_producer.last_sended.command.tenant_id == tenant_id
    assert fake_command_producer.last_sended.command.engine == "TESSERACT"


def test_parsing_service__unknown_parsing_type__error(
    document_mock,
    parsing_service,
    document_id,
    tenant_id,
):
    document_mock.get_brief_document_info.return_value = {
        "id": document_id,
        "title": "55130487",
        "state": "completed",
        "files": ["9af4d1792c2e42fab1be636a46aec200.png"],
        "typeId": "899948a1a50a4a059fd56863dd64dcdc",
        "engine": None,
        "language": None,
        "llmType": "dial@openai.gpt-3.5-turbo",
        "errorInState": None,
        "metadata": None,
    }

    with pytest.raises(UnsupportedParsingType):
        parsing_service.perform_parsing(
            document_id=document_id,
            tenant_id=tenant_id,
            features={},
            engine="HER",
        )


def test_get_command_channel__ok(document_type_repository_mock, parsing_service, test_document_type):
    document_type_repository_mock.find_by_id_for_tenant.return_value = test_document_type
    command_channel = parsing_service._get_command_channel(test_document_type.id(), test_document_type.tenant_id())

    assert command_channel == test_document_type.command_channel.name


def test_get_command_channel__no_saved_doc_types__return_none(
    document_type_repository_mock, parsing_service, test_document_type
):
    document_type_repository_mock.find_by_id_for_tenant.return_value = None
    command_channel = parsing_service._get_command_channel(test_document_type.id(), test_document_type.tenant_id())

    assert command_channel is None


def test_perform_parsing__document_type_provided__get_command_channel_called(
    fake_command_producer, document_type_repository_mock, parsing_service, tenant_id, document_id, test_document_type
):
    document_type_repository_mock.find_by_id_for_tenant.return_value = test_document_type
    parsing_service.perform_parsing(
        document_id=document_id,
        tenant_id=tenant_id,
        engine="TESSERACT",
        features={},
        document_type_id="doc_type_id",
    )

    assert document_type_repository_mock.find_by_id_for_tenant.called


def test_perform_parsing__document_type_provided__plugin_not_attached__no_errors(
    document_type_repository_mock,
    document_mock,
    document_layout_service_mock,
    parsing_service,
    tenant_id,
    document_id,
    test_document_type_without_command_channel,
):
    document_mock.get_brief_document_info.return_value = {
        "id": document_id,
        "title": "55130487",
        "state": "completed",
        "files": ["9af4d1792c2e42fab1be636a46aec200.docx"],
        "typeId": "899948a1a50a4a059fd56863dd64dcdc",
        "engine": None,
        "language": None,
        "llmType": "dial@openai.gpt-3.5-turbo",
        "errorInState": None,
        "metadata": None,
    }
    document_layout_service_mock.parse.return_value = EntityId()
    document_type_repository_mock.find_by_id_for_tenant.return_value = test_document_type_without_command_channel
    layout = parsing_service.perform_parsing(
        document_id=document_id,
        tenant_id=tenant_id,
        engine="TESSERACT",
        features={},
        document_type_id="doc_type_id",
    )

    assert layout


def test_perform_parsing__document_type_not_provided__get_command_channel_called__not_called(
    document_type_repository_mock,
    document_mock,
    document_layout_service_mock,
    parsing_service,
    tenant_id,
    document_id,
):
    document_mock.get_brief_document_info.return_value = {
        "id": document_id,
        "title": "55130487",
        "state": "completed",
        "files": ["9af4d1792c2e42fab1be636a46aec200.docx"],
        "typeId": "899948a1a50a4a059fd56863dd64dcdc",
        "engine": None,
        "language": None,
        "llmType": "dial@openai.gpt-3.5-turbo",
        "errorInState": None,
        "metadata": None,
    }

    document_type_repository_mock.find_by_id_for_tenant.return_value = None
    document_layout_service_mock.parse.return_value = EntityId()

    parsing_service.perform_parsing(document_id=document_id, tenant_id=tenant_id, engine="TESSERACT", features={})

    assert not document_type_repository_mock.find_by_id_for_tenant.called


@pytest.mark.parsing_info
def test_get_parsing_info__ok(
    document_layout_service_mock,
    document_layout,
    tabular_layout_service__with_mocked_excel_parser,
    saved_test_tabular_layout,
    parsing_service,
    tenant_id,
    document_layout_id,
):
    document_layout_service_mock.layout_info_for.return_value = document_layout
    parsing_info = parsing_service.get_parsing_info(document_id=document_layout_id, tenant_id=tenant_id)

    assert parsing_info.layout_id == document_layout_id
    assert parsing_info.document_layout_info == document_layout
    assert parsing_info.tabular_layout_info is not None


@pytest.mark.parsing_info
def test_get_parsing_info__only_dl__ok(
    document_layout_service_mock,
    tabular_layout_service__with_mocked_excel_parser,
    document_layout,
    parsing_service,
    tenant_id,
    document_layout_id,
):
    document_layout_service_mock.layout_info_for.return_value = document_layout
    parsing_info = parsing_service.get_parsing_info(document_id=document_layout_id, tenant_id=tenant_id)

    assert parsing_info.layout_id == document_layout_id
    assert parsing_info.document_layout_info == document_layout
    assert parsing_info.tabular_layout_info is None


@pytest.mark.parsing_info
def test_get_parsing_info__only_tl__ok(
    document_layout_service_mock,
    tabular_layout_service__with_mocked_excel_parser,
    fake_tl_query_repository,
    test_tabular_layout,
    parsing_service,
    tenant_id,
    document_layout_id,
):
    fake_tl_query_repository.save(test_tabular_layout)

    document_layout_service_mock.layout_info_for.return_value = None
    parsing_info = parsing_service.get_parsing_info(document_id=document_layout_id, tenant_id=tenant_id)

    assert parsing_info.layout_id == document_layout_id
    assert parsing_info.document_layout_info is None
    assert parsing_info.tabular_layout_info is not None


@pytest.mark.parsing_info
def test_get_parsing_info__not_tl__not_dl__ok(
    document_layout_service_mock,
    tabular_layout_service__with_mocked_excel_parser,
    parsing_service,
    tenant_id,
    document_layout_id,
):
    document_layout_service_mock.layout_info_for.return_value = None
    parsing_info = parsing_service.get_parsing_info(document_id=document_layout_id, tenant_id=tenant_id)

    assert parsing_info.layout_id == document_layout_id
    assert parsing_info.document_layout_info is None
    assert parsing_info.tabular_layout_info is None
