from azure.ai.formrecognizer import AnalyzeResult, DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

from .model_id import ModelId
from .settings import Settings

__all__ = ["AzureDocumentIntelligenceProxy"]


class AzureDocumentIntelligenceProxy:
    def __init__(self) -> None:
        settings = Settings()
        self._client = DocumentAnalysisClient(
            endpoint=settings.api_url,
            credential=AzureKeyCredential(settings.api_key),
        )

    def analyze_prebuilt_document(self, content: bytes) -> AnalyzeResult:
        poller = self._client.begin_analyze_document(model_id=ModelId.PREBUILT_DOCUMENT, document=content)

        return poller.result()

    def analyze_prebuilt_layout(self, content: bytes) -> AnalyzeResult:
        poller = self._client.begin_analyze_document(model_id=ModelId.PREBUILT_LAYOUT, document=content)

        return poller.result()
