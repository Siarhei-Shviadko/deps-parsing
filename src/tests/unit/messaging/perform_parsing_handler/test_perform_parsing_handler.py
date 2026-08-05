import pytest
from deps_document_layout.model import IDocumentLayoutRepository

from deps_parsing.domain.interfaces import ITabularLayoutQueryRepository
from deps_parsing.messaging.commands import ParseSemanticLayout
from deps_parsing.messaging.handlers import perform_parsing_handler


@pytest.mark.usefixtures("set_by_page_strategy", "prepare_dl_services", "save_content_to_storage")
def test_handler__no_parsing_features__by_page__parsing_skipped(perform_parsing_command_message_without_features):
    perform_parsing_handler(perform_parsing_command_message_without_features)


@pytest.mark.usefixtures("set_by_page_strategy", "prepare_dl_services")
def test_handler__dl__by_page__ok(
    dl_perform_parsing_command_message,
    document_layout_repository: IDocumentLayoutRepository,
    tenant_id,
    entity_id,
):
    perform_parsing_handler(dl_perform_parsing_command_message)

    assert document_layout_repository.is_layout_exists(layout_id=entity_id, tenant_id=tenant_id)


@pytest.mark.usefixtures("set_by_page_strategy", "prepare_tl_services")
def test_handler__tl__by_page__ok(
    tl_perform_parsing_command_message,
    fake_tl_command_repository: ITabularLayoutQueryRepository,
    tenant_id,
    entity_id,
):
    perform_parsing_handler(tl_perform_parsing_command_message)

    assert fake_tl_command_repository.layout_of_id(layout_id=entity_id, tenant_id=tenant_id)


@pytest.mark.usefixtures("set_by_document_strategy", "prepare_dl_services")
def test_handler__dl__by_document__ok(
    dl_perform_parsing_command_message,
    document_layout_repository: IDocumentLayoutRepository,
    tenant_id,
    entity_id,
):
    perform_parsing_handler(dl_perform_parsing_command_message)

    assert document_layout_repository.is_layout_exists(layout_id=entity_id, tenant_id=tenant_id)


@pytest.mark.usefixtures("set_by_document_strategy", "prepare_tl_services")
def test_handler__tl__by_document__ok(
    tl_perform_parsing_command_message,
    fake_tl_command_repository: ITabularLayoutQueryRepository,
    tenant_id,
    entity_id,
):
    perform_parsing_handler(tl_perform_parsing_command_message)

    assert fake_tl_command_repository.layout_of_id(layout_id=entity_id, tenant_id=tenant_id)


@pytest.mark.usefixtures("set_by_document_strategy", "prepare_dl_services", "save_docx_content_to_storage")
def test_handler__docx__by_document__dispatches_semantic_parsing(
    docx_perform_parsing_command_message,
    fake_command_producer,
    document_layout_repository: IDocumentLayoutRepository,
    tenant_id,
    entity_id,
):
    docx_perform_parsing_command_message.command.engine = "LLAMAINDEX"

    perform_parsing_handler(docx_perform_parsing_command_message)

    assert fake_command_producer.last_sended.channel == "SemanticParsingCommands"
    assert isinstance(fake_command_producer.last_sended.command, ParseSemanticLayout)
    assert fake_command_producer.last_sended.command.provider == "llamaindex"
    assert not document_layout_repository.is_layout_exists(layout_id=entity_id, tenant_id=tenant_id)


@pytest.mark.usefixtures("set_by_page_strategy", "prepare_dl_services", "save_docx_content_to_storage")
def test_handler__docx__by_page__dispatches_semantic_parsing(
    docx_perform_parsing_command_message,
    fake_command_producer,
    document_layout_repository: IDocumentLayoutRepository,
    tenant_id,
    entity_id,
):
    docx_perform_parsing_command_message.command.engine = "LLAMAINDEX"

    perform_parsing_handler(docx_perform_parsing_command_message)

    assert fake_command_producer.last_sended.channel == "SemanticParsingCommands"
    assert isinstance(fake_command_producer.last_sended.command, ParseSemanticLayout)
    assert fake_command_producer.last_sended.command.provider == "llamaindex"
    assert not document_layout_repository.is_layout_exists(layout_id=entity_id, tenant_id=tenant_id)
