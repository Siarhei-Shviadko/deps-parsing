import logging
from abc import ABC, abstractmethod
from typing import Any, Optional

from deps_document_layout.model import DocumentLayout, ParsingFeature, ParsingType

__all__ = ["IParseDocuments"]

RawResponse = dict[Any, Any]


class IParseDocuments(ABC):
    parsing_type: ParsingType
    processable_features: set[ParsingFeature]

    def __init__(self) -> None:
        self._logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def parse(
        self,
        document_layout: DocumentLayout,
        features: set[ParsingFeature],
        language: Optional[str] = None,
    ) -> tuple[DocumentLayout, Optional[RawResponse]]:
        ...

    def choose_processable_features(self, features: set[ParsingFeature]) -> set[ParsingFeature]:
        return self.processable_features.intersection(features)
