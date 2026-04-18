import pytest
from deps_message_flow.events.subscriber.domain_event_envelope import (
    DomainEventEnvelope,
)

from deps_parsing.application import DocumentLayoutService, TabularLayoutService
from deps_parsing.messaging.handlers import file_deleted_handler


@pytest.mark.document_layout
def test_handler__ok(
    tenant_id: str,
    file_deleted_envelope: DomainEventEnvelope,
    document_layout_service_mock: DocumentLayoutService,
    tabular_layout_service_mock: TabularLayoutService,
):
    document_layout_service_mock.delete_document_layout.return_value = None
    tabular_layout_service_mock.delete_layout.return_value = None

    file_deleted_handler(file_deleted_envelope)

    document_layout_service_mock.delete_document_layout.assert_called_once_with(
        file_deleted_envelope.event.id,
        tenant_id,
    )
    tabular_layout_service_mock.delete_layout.assert_called_once_with(file_deleted_envelope.event.id, tenant_id)
