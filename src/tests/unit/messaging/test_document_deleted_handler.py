import pytest
from deps_message_flow.events.subscriber.domain_event_envelope import (
    DomainEventEnvelope,
)

from deps_parsing.application import DocumentLayoutService, TabularLayoutService
from deps_parsing.domain.exceptions import BusinessException
from deps_parsing.messaging.handlers import document_deleted_handler


@pytest.mark.document_layout
def test_handler__ok(
    tenant_id: str,
    document_deleted_envelope: DomainEventEnvelope,
    document_layout_service_mock: DocumentLayoutService,
    tabular_layout_service_mock: TabularLayoutService,
):
    document_layout_service_mock.delete_document_layout.return_value = None
    tabular_layout_service_mock.delete_layout.return_value = None

    document_deleted_handler(document_deleted_envelope)
    document_layout_service_mock.delete_document_layout.assert_called_once_with(
        document_deleted_envelope.event.document_id,
        tenant_id,
    )
    tabular_layout_service_mock.delete_layout.assert_called_once_with(
        document_deleted_envelope.event.document_id,
        tenant_id,
    )


@pytest.mark.parametrize(
    "dl_side_effect,tl_side_effect",
    [
        (BusinessException("Some error"), None),
        (None, BusinessException("Some error")),
    ],
)
@pytest.mark.document_layout
def test_handler__business_error__intercepted(
    tenant_id: str,
    document_deleted_envelope: DomainEventEnvelope,
    document_layout_service_mock: DocumentLayoutService,
    tabular_layout_service_mock: TabularLayoutService,
    dl_side_effect,
    tl_side_effect,
):
    document_layout_service_mock.delete_document_layout.side_effect = dl_side_effect
    tabular_layout_service_mock.delete_layout.side_effect = tl_side_effect

    document_deleted_handler(document_deleted_envelope)

    if dl_side_effect:
        document_layout_service_mock.delete_document_layout.assert_called_once_with(
            document_deleted_envelope.event.document_id,
            tenant_id,
        )
        tabular_layout_service_mock.delete_layout.assert_not_called()
    else:
        document_layout_service_mock.delete_document_layout.assert_called_once_with(
            document_deleted_envelope.event.document_id,
            tenant_id,
        )
        tabular_layout_service_mock.delete_layout.assert_called_once_with(
            document_deleted_envelope.event.document_id,
            tenant_id,
        )


@pytest.mark.parametrize(
    "dl_side_effect,tl_side_effect",
    [
        (RuntimeError("Some error"), None),
        (None, RuntimeError("Some error")),
        (RuntimeError("Some error"), RuntimeError("Some error")),
    ],
)
@pytest.mark.document_layout
def test_handler__system_error__retried(
    tenant_id: str,
    document_deleted_envelope: DomainEventEnvelope,
    document_layout_service_mock: DocumentLayoutService,
    tabular_layout_service_mock: TabularLayoutService,
    dl_side_effect,
    tl_side_effect,
):
    document_layout_service_mock.delete_document_layout.side_effect = dl_side_effect
    tabular_layout_service_mock.delete_layout.side_effect = tl_side_effect

    with pytest.raises(RuntimeError):
        document_deleted_handler(document_deleted_envelope)

    document_layout_service_mock.delete_document_layout.assert_called_once_with(
        document_deleted_envelope.event.document_id,
        tenant_id,
    )

    if dl_side_effect is None:
        tabular_layout_service_mock.delete_layout.assert_called_once_with(
            document_deleted_envelope.event.document_id,
            tenant_id,
        )
