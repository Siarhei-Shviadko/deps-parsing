from azure.ai.formrecognizer import AnalyzeResult, DocumentPage

__all__ = ["FakeAzureProxy"]


class FakeAzureProxy:
    def __init__(self) -> None:
        self._result = AnalyzeResult(pages=[DocumentPage(page_number=1, width=1, height=1, unit="pxl")])

    def analyze_prebuilt_document(self, content: bytes) -> AnalyzeResult:
        return self._result

    def analyze_prebuilt_layout(self, content: bytes) -> AnalyzeResult:
        return self._result
