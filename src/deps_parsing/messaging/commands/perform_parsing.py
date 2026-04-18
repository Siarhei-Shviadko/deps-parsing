from dataclasses import dataclass
from typing import Optional

from deps_document_layout.model import ParsingFeature
from deps_message_flow.commands.common import Command

from ..error_type import ErrorType

__all__ = ["PerformParsing", "PerformParsingReply"]


@dataclass
class PerformParsing(Command):  # noqa: WPS230
    tenant_id: str
    document_id: str
    files: list[str]
    engine: Optional[str]
    features: Optional[list[ParsingFeature]] = None
    document_type_id: Optional[str] = None
    language: Optional[str] = None

    def __init__(
        self,
        tenant_id: str,
        document_id: str,
        files: list[str],
        engine: Optional[str],
        features: set[str],
        document_type_id: Optional[str] = None,
        language: Optional[str] = None,
    ):
        self.tenant_id = tenant_id
        self.document_id = document_id
        self.files = files
        self.engine = engine
        self.features = [ParsingFeature(feature) for feature in features] if features is not None else None
        self.document_type_id = document_type_id
        self.language = language


@dataclass
class PerformParsingReply(Command):
    error_type: Optional[ErrorType] = None
    error_message: Optional[str] = None
