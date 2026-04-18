from abc import ABC, abstractmethod
from typing import Any, Generic, Optional, TypeVar

from deps_document_layout.model import DocumentLayout, ParsingFeature, ParsingType
from deps_object_storage import ObjectStorage

from ...proxies import UnifiedDataImage, UnifierProxy
from ..abstract_engine import OCREngine
from ..image_processing import (
    OCRLayoutImageProcessingService,
    ParsedImage,
    PreparsedImage,
)
from .abstract_service import IParseDocuments

__all__ = ["PageOCRBasedParsingService", "OCRedPageRawResponse", "OCRedPageResponse"]

OCRedPageRawResponse = dict[int, Any]
OCRedPageResponse = TypeVar("OCRedPageResponse")


class PageOCRBasedParsingService(IParseDocuments, ABC, Generic[OCRedPageResponse]):
    parsing_type: ParsingType
    processable_features: set[ParsingFeature]

    def __init__(
        self,
        unifier: UnifierProxy,
        storage: ObjectStorage,
        engine: OCREngine,
        image_processing_service: OCRLayoutImageProcessingService,
    ) -> None:
        super().__init__()
        self._unifier = unifier
        self._storage = storage
        self._engine = engine
        self._image_processing_service = image_processing_service

    def parse(
        self,
        file_path: str,
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
            response: OCRedPageResponse = self.recognize_blob(blob, features, language)

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

    @abstractmethod
    def add_page_to_document_layout(
        self,
        document_layout: DocumentLayout,
        parsed_page: OCRedPageResponse,
        image: UnifiedDataImage,
        parsed_page_images: list[ParsedImage],
    ) -> None:
        ...

    @abstractmethod
    def add_page_to_raw_parsed_data(
        self,
        image: UnifiedDataImage,
        raw_page: OCRedPageResponse,
        raw_parsing_result: OCRedPageRawResponse,
    ) -> None:
        ...

    @abstractmethod
    def recognize_blob(
        self,
        blob: bytes,
        features: set[ParsingFeature],
        language: Optional[str] = None,
    ) -> OCRedPageResponse:
        ...

    def parse_images(
        self,
        layout_id: str,
        raw_page: bytes,
        parsed_page: OCRedPageResponse,
    ) -> list[ParsedImage]:
        preparsed_images = self._list_preparsed_images(layout_id, raw_page, parsed_page)

        return self._image_processing_service.process_preparsed_images(
            preparsed_images=preparsed_images,
        )

    @abstractmethod
    def _list_preparsed_images(
        self,
        layout_id: str,
        raw_page: bytes,
        parsed_page: OCRedPageResponse,
    ) -> list[PreparsedImage]:
        ...

    def _update_parsing_features(self, document_layout: DocumentLayout, features: set[ParsingFeature]) -> None:
        received_features = self._engine.fetch_received_features(features)
        document_layout.update_parsing_features(self.parsing_type, received_features)
