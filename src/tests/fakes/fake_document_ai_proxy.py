from deps_parsing.infrastructure.dl_parsing.google import DocAIDocument
from deps_parsing.infrastructure.proxies import GCPDocumentAIProxy

__all__ = ["FakeDocumentAIProxy"]


class FakeDocumentAIProxy(GCPDocumentAIProxy):
    def __init__(self, *args, **kwargs):
        self._response: DocAIDocument = DocAIDocument()
        self.last_called_content: bytes = b""
        self.last_called_mimetype: str = ""

    def perform_form_recognition(self, content: bytes, mime_type: str) -> DocAIDocument:
        self.last_called_content = content
        self.last_called_mimetype = mime_type

        return self.response

    def perform_full_document_recognition(
        self,
        gcs_input_uri: str,
        gcs_output_uri: str,
        mime_type: str = "application/pdf",
        timeout: int = 600,
    ) -> DocAIDocument:
        self.last_called_mimetype = mime_type

        return self.response

    @property
    def response(self):
        return self._response

    @response.setter
    def response(self, value: DocAIDocument):
        self._response = value
