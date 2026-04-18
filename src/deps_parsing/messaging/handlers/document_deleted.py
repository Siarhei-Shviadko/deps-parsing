import logging

from dependency_injector.wiring import Provide, inject
from deps_message_flow.events.subscriber.domain_event_envelope import (
    DomainEventEnvelope,
)

from deps_parsing.application import ParsingService
from deps_parsing.containers import Containers
from deps_parsing.domain.exceptions import BusinessException

__all__ = ["document_deleted_handler"]

logger = logging.getLogger(__name__)


@inject
def document_deleted_handler(
    dee: DomainEventEnvelope,
    parsing_service: ParsingService = Provide[Containers.applications.parsing_service],
    current_user_tenant: str = Provide[Containers.current_user_tenant],
):
    try:
        parsing_service.delete_layout(
            document_id=dee.event.document_id,
            tenant_id=current_user_tenant,
        )
    except BusinessException as err:
        logger.warning("Cannot delete layout `%s`. Reason: %r", dee.event.document_id, err)
