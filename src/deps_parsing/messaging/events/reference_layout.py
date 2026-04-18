from dataclasses import dataclass

from deps_message_flow.events.common import DomainEvent

__all__ = ["ReferenceLayoutDeleted"]


@dataclass
class ReferenceLayoutDeleted(DomainEvent):
    reference_layout_id: str
