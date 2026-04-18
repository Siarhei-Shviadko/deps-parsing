from typing import Optional

from deps_document_layout.model import EntityId, Guard, ImmutableCheck, TenantId

from ..command_channel import CommandChannel

__all__ = [
    "DocumentType",
]


class DocumentType:
    id = Guard[EntityId](EntityId, ImmutableCheck())
    tenant_id = Guard[TenantId](TenantId, ImmutableCheck())
    command_channel = Guard[CommandChannel](CommandChannel)

    def __init__(self, id_: EntityId, tenant_id: TenantId, command_channel: Optional[CommandChannel] = None) -> None:
        self.id = id_
        self.tenant_id = tenant_id
        if command_channel is not None:
            self.command_channel = command_channel

    def __eq__(self, other: object) -> bool:
        return isinstance(other, DocumentType) and other.id == self.id

    def attach_command_channel(self, name: str) -> None:
        self.command_channel = CommandChannel(name)
