from typing import Optional

from deps_document_layout.model import DocumentLayout, ParsingFeature, ParsingType

from deps_parsing.infrastructure.proxies import UnifiedDataImage

from ..image_processing import ParsedImage, PreparsedImage
from ..page_based_service import OCRedPageRawResponse, PageOCRBasedParsingService
from .engine import DepsStructuredResponse
from .parser import DepsParser

__all__ = ["BaseDepsParsingService"]


class BaseDepsParsingService(PageOCRBasedParsingService[DepsStructuredResponse]):
    parsing_type: ParsingType
    processable_features = {ParsingFeature.TEXT, ParsingFeature.TABLES}

    def add_page_to_document_layout(
        self,
        document_layout: DocumentLayout,
        parsed_page: DepsStructuredResponse,
        image: UnifiedDataImage,
        parsed_page_images: list[ParsedImage],
    ) -> None:
        DepsParser(
            image=image,
            parsing_type=self.parsing_type,
            language=parsed_page.language,
        ).add_response_to_page(
            parsed_page,
            document_layout,
        )

    def add_page_to_raw_parsed_data(
        self,
        image: UnifiedDataImage,
        raw_page: DepsStructuredResponse,
        raw_parsing_result: OCRedPageRawResponse,
    ) -> None:
        raw_parsing_result[image.page] = raw_page.orig_response

    def recognize_blob(
        self,
        blob: bytes,
        features: set[ParsingFeature],
        language: Optional[str] = None,
    ) -> DepsStructuredResponse:
        return DepsStructuredResponse(self._engine.recognize_blob(blob, features, language), language=language)

    def _list_preparsed_images(
        self,
        layout_id: str,
        raw_page: bytes,
        parsed_page: DepsStructuredResponse,
    ) -> list[PreparsedImage]:
        # Base OCR ain't able to parse images from file
        return []
