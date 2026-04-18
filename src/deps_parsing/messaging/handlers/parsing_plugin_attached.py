from dependency_injector.wiring import Provide, inject
from deps_message_flow.events.subscriber.domain_event_envelope import (
    DomainEventEnvelope,
)

from deps_parsing.application import DocumentTypeService
from deps_parsing.containers import Containers

__all__ = ["parsing_plugin_attached_handler"]


@inject
def parsing_plugin_attached_handler(
    dee: DomainEventEnvelope,
    service: DocumentTypeService = Provide[Containers.applications.document_type_service],
) -> None:
    service.attach_parsing_plugin(dee.event.document_type, dee.event.command_channel)
