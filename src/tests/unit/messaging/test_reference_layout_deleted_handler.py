import pytest

from deps_parsing.domain.exceptions import BusinessException
from deps_parsing.messaging.handlers import reference_layout_deleted_handler


@pytest.mark.document_layout
def test_handler__ok(reference_layout_deleted_envelope, document_layout_service_mock, tenant_id):
    document_layout_service_mock.delete_document_layout.return_valuer = None

    reference_layout_deleted_handler(reference_layout_deleted_envelope)

    document_layout_service_mock.delete_document_layout.assert_called_once_with(
        document_layout_id=reference_layout_deleted_envelope.event.reference_layout_id,
        tenant_id=tenant_id,
    )


@pytest.mark.document_layout
def test_handler__business_error__intercepted(
    reference_layout_deleted_envelope,
    document_layout_service_mock,
    tenant_id,
):
    document_layout_service_mock.delete_document_layout.side_effect = BusinessException("Some error")

    reference_layout_deleted_handler(reference_layout_deleted_envelope)

    document_layout_service_mock.delete_document_layout.assert_called_once_with(
        document_layout_id=reference_layout_deleted_envelope.event.reference_layout_id,
        tenant_id=tenant_id,
    )


@pytest.mark.document_layout
def test_handler__system_error__retried(
    reference_layout_deleted_envelope,
    document_layout_service_mock,
    tenant_id,
):
    document_layout_service_mock.delete_document_layout.side_effect = RuntimeError("Some error")

    with pytest.raises(RuntimeError):
        reference_layout_deleted_handler(reference_layout_deleted_envelope)

    document_layout_service_mock.delete_document_layout.assert_called_once_with(
        document_layout_id=reference_layout_deleted_envelope.event.reference_layout_id,
        tenant_id=tenant_id,
    )
