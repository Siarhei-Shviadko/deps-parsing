from typing import Any

from deps_document_layout.model import EntityId, TenantId

from deps_parsing.domain.model import CommandChannel, DocumentType

__all__ = ["DocumentTypeMapper"]


class DocumentTypeMapper:
    @classmethod
    def to_dict(cls, document_type: DocumentType) -> dict[str, Any]:
        return {
            "id": document_type.id(),
            "tenant_id": document_type.tenant_id(),
            "command_channel": document_type.command_channel.name
            if document_type.command_channel is not None
            else None,
        }

    @classmethod
    def from_dict(cls, document_type: dict[str, Any]) -> DocumentType:
        return DocumentType(
            id_=EntityId(document_type["id"]),
            tenant_id=TenantId(document_type["tenant_id"]),
            command_channel=CommandChannel(document_type["command_channel"])
            if document_type["command_channel"] is not None
            else None,
        )
