from contextlib import contextmanager
from typing import Any, Generator

from deps_document_layout.model import DocumentLayout, ParsingFeature, ParsingType
from deps_object_storage import ObjectStorage, make_gcp_object_storage
from deps_object_storage.settings import Settings

from ....proxies import UnifiedDataImage, UnifierProxy
from ...google import (
    DocAIDocument,
    DocAIPage,
    DocumentAIEngine,
    DocumentAIResponseParser,
)
from ...image_processing import (
    OCRLayoutImageProcessingService,
    ParsedImage,
    PreparsedImage,
)
from ..document_based_service import DocumentOCRBasedParsingService

__all__ = ["DocumentAIDocumentParsingService"]


class DocumentAIDocumentParsingService(DocumentOCRBasedParsingService[DocAIDocument]):
    parsing_type = ParsingType.GCP_VISION
    processable_features = {
        ParsingFeature.TEXT,
        ParsingFeature.KEY_VALUE_PAIRS,
        ParsingFeature.TABLES,
    }

    def __init__(
        self,
        unifier: UnifierProxy,
        storage: ObjectStorage,
        engine: DocumentAIEngine,
        image_processing_service: OCRLayoutImageProcessingService,
        output_directory: str,
    ) -> None:
        super().__init__(storage=storage, engine=engine, image_processing_service=image_processing_service)
        self._unifier = unifier
        self._init_google_storage()
        self._output_directory = output_directory

    def parse(
        self,
        file_path: str,
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

        with self._gcp_blob_name(file_path) as input_uri:
            self._logger.info(f"Processing file {input_uri}")
            filename = input_uri.split("/")[-1]

            docai_document: DocAIDocument = self._engine.recognize_document(
                gcs_input_uri=input_uri,
                gcs_output_uri=self._output_directory,
                filename=filename,
            )
            pages_map = {page.page_number: page for page in docai_document.pages}

            for image in self._unifier.get_original_images(document_id=document_layout.id()):
                docai_page = pages_map.get(image.page)
                if not docai_page:
                    self._logger.warning(
                        f"No matching page {image.page} found in docai_document for image {image.blob_name}",
                    )
                    continue

                parsed_page_images = self._parse_images_with_page(
                    layout_id=document_layout.id(),
                    raw_page=None,
                    docai_page=docai_page,
                )

                self._add_page_to_document_layout(
                    document_layout=document_layout,
                    image=image,
                    docai_document=docai_document,
                    docai_page=docai_page,
                    parsed_page_images=parsed_page_images,
                )

            self._update_parsing_features(document_layout, features)

            return document_layout, DocAIDocument.to_dict(docai_document, use_integers_for_enums=False)

    def add_to_document_layout(
        self,
        document_layout: DocumentLayout,
        parsed_document: DocAIDocument,
        parsed_images: list[ParsedImage],
    ) -> None:
        raise NotImplementedError

    def recognize_blob(
        self,
        blob: bytes,
        features: set[ParsingFeature],
        language: str | None = None,
    ) -> DocAIDocument:
        raise NotImplementedError

    def _add_page_to_document_layout(
        self,
        document_layout: DocumentLayout,
        image: UnifiedDataImage,
        docai_document: DocAIDocument,
        docai_page: DocAIPage,
        parsed_page_images: list[ParsedImage],
    ) -> None:
        self._logger.info(f"Adding page {docai_page.page_number} to document layout")
        DocumentAIResponseParser(docai_document, docai_page, image).add_page_to(document_layout)

    def _list_preparsed_images(
        self,
        layout_id: str,
        raw_document: bytes,
        parsed_document: DocAIDocument,
    ) -> list[PreparsedImage]:
        raise NotImplementedError

    def _parse_images_with_page(
        self,
        layout_id: str,
        raw_page: bytes | None,
        docai_page: DocAIPage,
    ) -> list[ParsedImage]:
        # Can be implemented later if needed
        preparsed_images = []  # type: ignore
        return self._image_processing_service.process_preparsed_images(
            preparsed_images=preparsed_images,
        )

    def _init_google_storage(self) -> None:
        self.object_storage_settings = Settings()
        if self.object_storage_settings.type == "gcp":
            self._gcp_object_storage = self._storage
        else:
            self._gcp_object_storage = make_gcp_object_storage(self.object_storage_settings.mode)

    @contextmanager
    def _gcp_blob_name(self, file_path: str) -> Generator[str, None, None]:
        uploaded = False

        if self.object_storage_settings.type == "gcp":
            blob_name = file_path
        else:
            document_content = self._fetch_blob(file_path)
            blob_name = self._gcp_object_storage.upload(
                path=file_path,
                content=document_content,
                replace_if_exists=True,
            )
            uploaded = True

        try:
            yield blob_name
        finally:
            if uploaded:
                self._gcp_object_storage.delete(blob_name)
