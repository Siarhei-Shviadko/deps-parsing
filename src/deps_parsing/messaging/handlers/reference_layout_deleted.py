import logging

from dependency_injector.wiring import Provide, inject
from deps_message_flow.events.subscriber.domain_event_envelope import (
    DomainEventEnvelope,
)

from deps_parsing.api import get_current_user_tenant
from deps_parsing.application import DocumentLayoutService
from deps_parsing.containers import Containers
from deps_parsing.domain.exceptions import BusinessException

__all__ = ["reference_layout_deleted_handler"]

logger = logging.getLogger(__name__)


@inject
def reference_layout_deleted_handler(
    dee: DomainEventEnvelope,
    document_layout_service: DocumentLayoutService = Provide[Containers.applications.document_layout_service],
):
    document_layout_id = dee.event.reference_layout_id
    try:
        document_layout_service.delete_document_layout(
            document_layout_id=document_layout_id,
            tenant_id=get_current_user_tenant(),
        )
    except BusinessException as err:
        logger.warning("Cannot delete document layout `%s`. Reason: %r", document_layout_id, err)
