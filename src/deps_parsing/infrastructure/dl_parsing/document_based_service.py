from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor, as_completed
from contextvars import copy_context
from typing import Any, Generic, TypeVar

from deps_document_layout.model import DocumentLayout, ParsingFeature, ParsingType
from deps_object_storage import ObjectStorage

from ..exceptions import EntityNotFoundError
from ..proxies import DocumentProxy, FileProxy, UnifierProxy
from .abstract_engine import OCREngine
from .abstract_service import IParseDocuments
from .image_processing import (
    OCRLayoutImageProcessingService,
    ParsedImage,
    PreparsedImage,
)

__all__ = ["DocumentOCRBasedParsingService", "OCRedDocumentResponse"]

OCRedDocumentResponse = TypeVar("OCRedDocumentResponse")


class DocumentOCRBasedParsingService(IParseDocuments, ABC, Generic[OCRedDocumentResponse]):
    parsing_type: ParsingType
    processable_features: set[ParsingFeature]

    def __init__(
        self,
        unifier: UnifierProxy,
        storage: ObjectStorage,
        engine: OCREngine,
        image_processing_service: OCRLayoutImageProcessingService,
        document: DocumentProxy,
        file: FileProxy,
    ) -> None:
        super().__init__()
        self._unifier = unifier
        self._storage = storage
        self._engine = engine
        self._image_processing_service = image_processing_service
        self._document = document
        self._file = file

    def parse(
        self,
        document_layout: DocumentLayout,
        features: set[ParsingFeature],
        language: str | None = None,
    ) -> tuple[DocumentLayout, dict[str, Any]]:
        self._logger.info(
            "Document analyzing for document layout %s with features %s and language %s has been started",
            document_layout.id(),
            [feature.value for feature in features],
            language,
        )

        blob = self._fetch_blob(document_layout.id())
        response: OCRedDocumentResponse = self.recognize_blob(blob, features, language)  # type: ignore

        self.add_to_document_layout(
            document_layout=document_layout,
            parsed_document=response,
            parsed_images=self.parse_images(
                layout_id=document_layout.id(),
                raw_document=blob,
                parsed_document=response,
            ),
        )

        self._update_parsing_features(document_layout, features)

        return document_layout, response.to_dict()

    @abstractmethod
    def add_to_document_layout(
        self,
        document_layout: DocumentLayout,
        parsed_document: OCRedDocumentResponse,
        parsed_images: list[ParsedImage],
    ) -> None:
        ...  # noqa: WPS428

    @abstractmethod
    def recognize_blob(
        self,
        blob: bytes,
        features: set[ParsingFeature],
        language: str | None = None,
    ) -> OCRedDocumentResponse:
        ...  # noqa: WPS428

    def parse_images(
        self,
        layout_id: str,
        raw_document: bytes,
        parsed_document: OCRedDocumentResponse,
    ) -> list[ParsedImage]:
        preparsed_images = self._list_preparsed_images(layout_id, raw_document, parsed_document)

        return self._image_processing_service.process_preparsed_images(
            preparsed_images=preparsed_images,
        )

    @abstractmethod
    def _list_preparsed_images(
        self,
        layout_id: str,
        raw_document: bytes,
        parsed_document: OCRedDocumentResponse,
    ) -> list[PreparsedImage]:
        ...  # noqa: WPS428

    def _fetch_blob(self, entity_id: str) -> bytes:
        context = copy_context()

        def fetch_from_document() -> bytes:  # noqa: WPS430
            return self._document.get_document_files(document_id=entity_id)

        def fetch_from_file() -> bytes:  # noqa: WPS430
            return self._file.get_file_content(file_id=entity_id)

        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(context.run, fetch_from_document),
                executor.submit(context.run, fetch_from_file),
            ]

            for future in as_completed(futures):
                try:
                    return future.result()
                except Exception:  # noqa: S110
                    pass

        raise EntityNotFoundError(f"Entity {entity_id} not found")

    def _update_parsing_features(self, document_layout: DocumentLayout, features: set[ParsingFeature]) -> None:
        received_features = self._engine.fetch_received_features(features)
        document_layout.update_parsing_features(self.parsing_type, received_features)

    def _get_blob_name(self, document_detail: dict[str, Any]) -> str:
        for file_blob_name in document_detail.get("files", []):  # noqa: WPS328
            return file_blob_name

        document_id = document_detail.get("id")
        raise ValueError(f"Cannot find blob name for document {document_id}")
