from typing import Optional

from azure.ai.formrecognizer import AnalyzeResult
from deps_document_layout.model import DocumentLayout, ParsingFeature, ParsingType

from ...proxies import UnifiedDataImage
from ..image_processing import ParsedImage, PreparsedImage
from ..page_based_service import OCRedPageRawResponse, PageOCRBasedParsingService
from .parser import AzureParser

__all__ = ["AzurePageParsingService"]


class AzurePageParsingService(PageOCRBasedParsingService[AnalyzeResult]):
    parsing_type = ParsingType.AZURE_FORM_RECOGNIZER
    processable_features = {ParsingFeature.TEXT, ParsingFeature.TABLES, ParsingFeature.KEY_VALUE_PAIRS}

    def add_page_to_document_layout(
        self,
        document_layout: DocumentLayout,
        parsed_page: AnalyzeResult,
        image: UnifiedDataImage,
        parsed_page_images: list[ParsedImage],
    ) -> None:
        AzureParser(parsed_page, [image]).add_pages_to(document_layout)

    def recognize_blob(
        self,
        blob: bytes,
        features: set[ParsingFeature],
        language: Optional[str] = None,
    ) -> AnalyzeResult:
        return self._engine.recognize_blob(blob, features)

    def add_page_to_raw_parsed_data(
        self,
        image: UnifiedDataImage,
        raw_page: AnalyzeResult,
        raw_parsing_result: OCRedPageRawResponse,
    ) -> None:
        raw_parsing_result[image.page] = raw_page.to_dict()

    def _list_preparsed_images(
        self,
        layout_id: str,
        raw_page: bytes,
        parsed_page: AnalyzeResult,
    ) -> list[PreparsedImage]:
        # might be implemented in the future if needed
        return []
