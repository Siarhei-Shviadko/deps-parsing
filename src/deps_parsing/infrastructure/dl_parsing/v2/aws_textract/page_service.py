from typing import Optional

from deps_document_layout.model import DocumentLayout, ParsingFeature, ParsingType
from textractor.data.constants import LAYOUT_FIGURE

from ....proxies import UnifiedDataImage
from ...aws_textract import AWSTextractDocument, AwsTextractParser, StructuredResponse
from ...image_processing import ParsedImage, PreparsedImage
from ..page_based_service import OCRedPageRawResponse, PageOCRBasedParsingService

__all__ = ["AWSTextractPageParsingService"]


class AWSTextractPageParsingService(PageOCRBasedParsingService[AWSTextractDocument]):
    parsing_type = ParsingType.AWS_TEXTRACT
    processable_features = {
        ParsingFeature.TEXT,
        ParsingFeature.KEY_VALUE_PAIRS,
        ParsingFeature.TABLES,
        ParsingFeature.IMAGES,
    }

    def add_page_to_document_layout(
        self,
        document_layout: DocumentLayout,
        parsed_page: AWSTextractDocument,
        image: UnifiedDataImage,
        parsed_page_images: list[ParsedImage],
    ) -> None:
        for aws_page in parsed_page.pages:
            AwsTextractParser(aws_page, image, parsed_page_images).add_page_to(document_layout)

    def add_page_to_raw_parsed_data(
        self,
        image: UnifiedDataImage,
        raw_page: AWSTextractDocument,
        raw_parsing_result: OCRedPageRawResponse,
    ) -> None:
        raw_parsing_result[image.page] = raw_page.response

    def recognize_blob(
        self,
        blob: bytes,
        features: set[ParsingFeature],
        language: Optional[str] = None,
    ) -> AWSTextractDocument:
        return self._engine.recognize_blob(blob, features, language)

    def _list_preparsed_images(
        self,
        layout_id: str,
        raw_page: bytes,
        parsed_page: AWSTextractDocument,
    ) -> list[PreparsedImage]:
        return [
            PreparsedImage(
                layout_id=layout_id,
                page_image=raw_page,
                polygon=StructuredResponse.polygon_of(image),
            )
            for image in StructuredResponse.list_layout_by_type(parsed_page, layout_type=LAYOUT_FIGURE)
        ]
