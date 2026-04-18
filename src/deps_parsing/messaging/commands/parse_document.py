from dataclasses import dataclass
from typing import Optional

from deps_document_layout.model import ParsingFeature
from deps_message_flow.commands.common import Command

__all__ = ["ParseDocument"]


@dataclass
class ParseDocument(Command):
    document_id: str
    tenant_id: str
    engine: str
    features: list[ParsingFeature]
    language: Optional[str] = None
