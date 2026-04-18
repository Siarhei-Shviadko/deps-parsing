import logging

from dependency_injector.wiring import Provide, inject
from deps_message_flow.events.subscriber.domain_event_envelope import (
    DomainEventEnvelope,
)

from deps_parsing.application import TabularLayoutService
from deps_parsing.containers import Containers
from deps_parsing.domain.exceptions import BusinessException

__all__ = ["tabular_layout_deleted_handler"]

logger = logging.getLogger(__name__)


@inject
def tabular_layout_deleted_handler(
    dee: DomainEventEnvelope,
    tabular_layout_service: TabularLayoutService = Provide[Containers.applications.tabular_layout_service],
):
    try:
        tabular_layout_service.delete_layout_cells(
            layout_id=dee.event.id,
        )
    except BusinessException as err:
        logger.error("Cannot delete cells belong to tabular layout `%s`. Reason: %r", dee.event.id, err)
