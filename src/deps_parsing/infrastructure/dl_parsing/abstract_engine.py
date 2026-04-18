from typing import Any, Optional, Protocol

from deps_document_layout.model import ParsingFeature

__all__ = ["OCREngine"]


class OCREngine(Protocol):
    def recognize_blob(
        self,
        blob: bytes,
        features: set[ParsingFeature],
        language: Optional[str] = None,
        filename: Optional[str] = None,
    ) -> Any:
        pass

    def fetch_received_features(self, features: set[ParsingFeature]) -> set[ParsingFeature]:
        pass
