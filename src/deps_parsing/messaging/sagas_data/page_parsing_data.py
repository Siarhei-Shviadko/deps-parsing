from typing import Any, Optional
from uuid import uuid4

from deps_document_layout.model import ParsingFeature, ParsingType
from deps_message_flow.sagas.orchestration import SagaData

__all__ = ["PageParsingSagaData"]


class PageParsingSagaData(SagaData):
    def __init__(
        self,
        blob: bytes,
        parsing_type: ParsingType,
        features: set[ParsingFeature],
        language: Optional[str] = None,
    ):
        super().__init__(entity_id=uuid4().hex)
        self.blob = blob
        self.parsing_type = parsing_type
        self.features = features
        self.language = language

        self.parsing_result: dict[str, Any] = {}

    @property
    def tables_extraction_is_needed(self) -> bool:
        return ParsingFeature.TABLES in self.features
