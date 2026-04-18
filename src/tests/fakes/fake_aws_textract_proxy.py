from typing import Any

from deps_document_layout.model import ParsingFeature

from deps_parsing.infrastructure import AWSTextractProxy

__all__ = ["FakeAWSTextractProxy"]


class FakeAWSTextractProxy(AWSTextractProxy):
    def __init__(self, *args, **kwargs):
        self._response: dict[str, Any] = {"DocumentMetadata": {"Pages": 0}, "Blocks": []}
        self.last_called_content: bytes = b""
        self.last_called_features: list[ParsingFeature] = []

    def analyze_document_with_features(self, content: bytes, features: list[ParsingFeature]) -> dict:
        self.last_called_content = content
        self.last_called_features = features
        return self.response

    def async_analyze_document_with_features(
        self,
        bucket_name: str,
        key: str,
        features: list[ParsingFeature],
    ) -> dict:
        self.last_called_features = features
        return self.response

    @property
    def response(self):
        return self._response

    @response.setter
    def response(self, value: dict):
        self._response = value
