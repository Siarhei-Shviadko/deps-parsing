from typing import Optional

from deps_document_layout.model import DocumentLayout, ParsingFeature, ParsingType

from ...proxies import UnifiedDataImage
from ..image_processing import ParsedImage, PreparsedImage
from ..page_based_service import OCRedPageRawResponse, PageOCRBasedParsingService
from .parser import DocAIDocument, DocumentAIResponseParser

__all__ = ["DocumentAIPageParsingService"]


class DocumentAIPageParsingService(PageOCRBasedParsingService[DocAIDocument]):
    parsing_type = ParsingType.GCP_VISION
    processable_features = {
        ParsingFeature.TEXT,
        ParsingFeature.KEY_VALUE_PAIRS,
        ParsingFeature.TABLES,
    }

    def parse(
        self,
        document_layout: DocumentLayout,
        features: set[ParsingFeature],
        language: Optional[str] = None,
    ) -> tuple[DocumentLayout, OCRedPageRawResponse]:
        self._logger.info(
            "Document analyzing for document layout %s with features %s and language %s has been started",
            document_layout.id(),
            [feature.value for feature in features],
            language,
        )

        raw_page_responses: OCRedPageRawResponse = {}

        for image in self._unifier.get_original_images(document_id=document_layout.id()):
            blob = self._storage.download(path=image.blob_name)

            response: DocAIDocument = self.recognize_blob(
                blob=blob,
                features=features,
                language=language,
                filename=image.blob_name,
            )

            parsed_page_images = self.parse_images(
                layout_id=document_layout.id(),
                raw_page=blob,
                parsed_page=response,
            )

            self.add_page_to_document_layout(
                document_layout=document_layout,
                parsed_page=response,
                image=image,
                parsed_page_images=parsed_page_images,
            )

            self.add_page_to_raw_parsed_data(image, raw_parsing_result=raw_page_responses, raw_page=response)

        self._update_parsing_features(document_layout, features)

        return document_layout, raw_page_responses

    def add_page_to_document_layout(
        self,
        document_layout: DocumentLayout,
        parsed_page: DocAIDocument,
        image: UnifiedDataImage,
        parsed_page_images: list[ParsedImage],
    ) -> None:
        for gcp_page in parsed_page.pages:
            DocumentAIResponseParser(parsed_page, gcp_page, image).add_page_to(document_layout)

    def add_page_to_raw_parsed_data(
        self,
        image: UnifiedDataImage,
        raw_page: DocAIDocument,
        raw_parsing_result: OCRedPageRawResponse,
    ) -> None:
        raw_document = DocAIDocument.to_dict(raw_page, use_integers_for_enums=False)

        # GCP places here large base64 string, which we don't need
        for page in raw_document["pages"]:
            page["image"]["content"] = ""

        raw_parsing_result[image.page] = raw_document

    def recognize_blob(
        self,
        blob: bytes,
        features: set[ParsingFeature],
        language: Optional[str] = None,
        filename: str = None,
    ) -> DocAIDocument:
        return self._engine.recognize_blob(blob, features, language, filename)

    def _list_preparsed_images(
        self,
        layout_id: str,
        raw_page: bytes,
        parsed_page: DocAIDocument,
    ) -> list[PreparsedImage]:
        # Can be implemented later if needed
        return []
