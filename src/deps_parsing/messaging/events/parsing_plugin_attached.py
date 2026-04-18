from dataclasses import dataclass

from deps_message_flow.events.common import DomainEvent

__all__ = ["ParsingPluginAttached"]


@dataclass
class ParsingPluginAttached(DomainEvent):
    document_type: str
    command_channel: str
