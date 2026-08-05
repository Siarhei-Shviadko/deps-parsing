from dataclasses import dataclass
from typing import Optional

from deps_document_layout.model import ParsingFeature
from deps_message_flow.commands.common import Command

__all__ = ["ParseSemanticLayout"]


@dataclass
class ParseSemanticLayout(Command):
    entity_id: str
    tenant_id: str
    file_path: str
    provider: str
    features: Optional[list[ParsingFeature]] = None
    language: Optional[str] = None
