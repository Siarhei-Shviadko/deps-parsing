from typing import Optional

from azure.ai.formrecognizer import AnalyzeResult
from deps_document_layout.model import ParsingFeature

from deps_parsing.infrastructure.proxies import AzureDocumentIntelligenceProxy

from ..abstract_engine import OCREngine

__all__ = ["AzureOCREngine"]


class AzureOCREngine(OCREngine):
    def __init__(self, proxy: AzureDocumentIntelligenceProxy) -> None:
        self._proxy = proxy

    def recognize_blob(
        self,
        blob: bytes,
        features: set[ParsingFeature],
        language: Optional[str] = None,
        filename: Optional[str] = None,
    ) -> AnalyzeResult:
        if ParsingFeature.KEY_VALUE_PAIRS in features:
            return self._proxy.analyze_prebuilt_document(blob)

        return self._proxy.analyze_prebuilt_layout(blob)

    def fetch_received_features(self, features: set[ParsingFeature]) -> set[ParsingFeature]:
        if ParsingFeature.KEY_VALUE_PAIRS in features:
            return {ParsingFeature.TEXT, ParsingFeature.TABLES, ParsingFeature.KEY_VALUE_PAIRS}

        return {ParsingFeature.TEXT, ParsingFeature.TABLES}
