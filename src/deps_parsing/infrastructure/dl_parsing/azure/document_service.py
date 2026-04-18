from azure.ai.formrecognizer import AnalyzeResult
from deps_document_layout.model import DocumentLayout, ParsingFeature, ParsingType

from deps_parsing.infrastructure.dl_parsing.image_processing import ParsedImage

from ..document_based_service import (
    DocumentOCRBasedParsingService,
    OCRedDocumentResponse,
)
from ..image_processing import PreparsedImage
from .parser import AzureParser

__all__ = ["AzureDocumentParsingService"]


class AzureDocumentParsingService(DocumentOCRBasedParsingService[AnalyzeResult]):
    parsing_type = ParsingType(ParsingType.AZURE_FORM_RECOGNIZER)
    processable_features = {ParsingFeature.TEXT, ParsingFeature.TABLES, ParsingFeature.KEY_VALUE_PAIRS}

    def recognize_blob(self, blob: bytes, features: set[ParsingFeature], language: str | None = None) -> AnalyzeResult:
        return self._engine.recognize_blob(blob, features)

    def add_to_document_layout(
        self,
        document_layout: DocumentLayout,
        parsed_document: AnalyzeResult,
        parsed_images: list[ParsedImage],
    ) -> None:
        unified_images = self._unifier.get_original_images(document_id=document_layout.id())
        AzureParser(parsed_document, unified_images).add_pages_to(document_layout)

    def _list_preparsed_images(
        self,
        layout_id: str,
        raw_document: bytes,
        parsed_document: OCRedDocumentResponse,
    ) -> list[PreparsedImage]:
        # might be implemented in the future if needed
        return []
