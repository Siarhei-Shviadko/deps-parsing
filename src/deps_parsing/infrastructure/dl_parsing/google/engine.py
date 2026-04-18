import mimetypes
from typing import Optional

from deps_document_layout.model import ParsingFeature

from deps_parsing.infrastructure.proxies import GCPDocumentAIProxy

from ..abstract_engine import OCREngine
from .parser.types import DocAIDocument

__all__ = ["DocumentAIEngine"]

_DEFAULT_MIMETYPE = "application/pdf"


def _guess_mimetype(filename: Optional[str]) -> str:
    if not filename:
        return _DEFAULT_MIMETYPE

    return mimetypes.guess_type(filename)[0] or _DEFAULT_MIMETYPE


class DocumentAIEngine(OCREngine):
    def __init__(self, document_ai_proxy: GCPDocumentAIProxy) -> None:
        self._document_ai_proxy = document_ai_proxy

    def recognize_blob(
        self,
        blob: bytes,
        features: set[ParsingFeature],
        language: Optional[str] = None,
        filename: Optional[str] = None,
    ) -> DocAIDocument:
        mimetype = _guess_mimetype(filename)

        return self._document_ai_proxy.perform_form_recognition(blob, mimetype)

    def recognize_document(
        self,
        gcs_input_uri: str,
        gcs_output_uri: str,
        filename: Optional[str] = None,
    ) -> DocAIDocument:
        mimetype = _guess_mimetype(filename)

        return self._document_ai_proxy.perform_full_document_recognition(
            gcs_input_uri=gcs_input_uri,
            gcs_output_uri=gcs_output_uri,
            mime_type=mimetype,
        )

    def fetch_received_features(self, features: set[ParsingFeature]) -> set[ParsingFeature]:
        """
        We always use all possible features - performing Form Recognition task.
        Because Document Layout Parsing processors are very limited
        - they don't extract coordinates;
        - they don't handle images (png, jpg, etc.);
        - they don't have confidence;
        - they don't make page level analysis.
        """
        return {ParsingFeature.TEXT, ParsingFeature.TABLES, ParsingFeature.KEY_VALUE_PAIRS}
