from typing import Optional

from deps_document_layout.model import EntityId, TenantId

from ..command_channel import CommandChannel
from .document_type import DocumentType

__all__ = ["DocumentTypeFactory"]


class DocumentTypeFactory:
    @staticmethod
    def create(document_type_id: str, tenant_id: str, command_channel: Optional[str] = None) -> DocumentType:
        return DocumentType(
            id_=EntityId(document_type_id),
            tenant_id=TenantId(tenant_id),
            command_channel=CommandChannel(command_channel) if command_channel else None,
        )
