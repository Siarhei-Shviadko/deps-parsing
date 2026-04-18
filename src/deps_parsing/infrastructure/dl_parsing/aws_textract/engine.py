from typing import Any, Optional

from deps_document_layout.model import ParsingFeature
from textractor.parsers import response_parser

from deps_parsing.infrastructure.proxies import AWSTextractProxy

from ..abstract_engine import OCREngine

__all__ = ["AWSTextractEngine"]


class AWSTextractEngine(OCREngine):
    def __init__(self, aws_textract_proxy: AWSTextractProxy):
        self._textract_proxy = aws_textract_proxy

    def recognize_blob(
        self,
        blob: bytes,
        features: set[ParsingFeature],
        language: Optional[str] = None,
        filename: Optional[str] = None,
    ) -> Any:
        response = self._textract_proxy.analyze_document_with_features(blob, [*features])  # noqa: WPS356
        return response_parser.parse(response)

    def fetch_received_features(self, features: set[ParsingFeature]) -> set[ParsingFeature]:
        always_enabled_features = {ParsingFeature.TEXT}
        amazon_gift_features = self._get_amazon_gift_features(features)
        return features.union(always_enabled_features).union(amazon_gift_features)

    def recognize_document(
        self,
        bucket_name: str,
        key: str,
        features: list[ParsingFeature],
    ) -> dict[str, Any]:
        return self._textract_proxy.async_analyze_document_with_features(
            bucket_name=bucket_name,
            key=key,
            features=features,
        )

    @staticmethod
    def _get_amazon_gift_features(features: set[ParsingFeature]) -> set[ParsingFeature]:
        if {ParsingFeature.KEY_VALUE_PAIRS, ParsingFeature.TABLES}.intersection(features):
            return {ParsingFeature.IMAGES}
        return set()
