from azure.ai.formrecognizer import AnalyzeResult
from deps_document_layout.model import DocumentLayout, ParsingFeature, ParsingType
from deps_object_storage import ObjectStorage

from ....proxies import UnifierProxy
from ...azure import AzureOCREngine, AzureParser
from ...image_processing import (
    OCRLayoutImageProcessingService,
    ParsedImage,
    PreparsedImage,
)
from ..document_based_service import (
    DocumentOCRBasedParsingService,
    OCRedDocumentResponse,
)

__all__ = ["AzureDocumentParsingService"]


class AzureDocumentParsingService(DocumentOCRBasedParsingService[AnalyzeResult]):
    parsing_type = ParsingType(ParsingType.AZURE_FORM_RECOGNIZER)
    processable_features = {ParsingFeature.TEXT, ParsingFeature.TABLES, ParsingFeature.KEY_VALUE_PAIRS}

    def __init__(
        self,
        unifier: UnifierProxy,
        storage: ObjectStorage,
        engine: AzureOCREngine,
        image_processing_service: OCRLayoutImageProcessingService,
    ) -> None:
        super().__init__(storage=storage, engine=engine, image_processing_service=image_processing_service)
        self._unifier = unifier

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
