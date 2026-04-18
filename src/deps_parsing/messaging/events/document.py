from dataclasses import dataclass

from deps_message_flow.events.common import DomainEvent

__all__ = ["DocumentDeleted"]


@dataclass
class DocumentDeleted(DomainEvent):
    document_id: int
