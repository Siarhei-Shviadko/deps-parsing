from concurrent.futures import Future, ThreadPoolExecutor
from contextlib import contextmanager
from contextvars import copy_context
from typing import Any, Callable, Generator

from deps_document_layout.model import DocumentLayout, ParsingFeature, ParsingType
from deps_object_storage import ObjectStorage, make_aws_object_storage
from deps_object_storage.settings import Settings
from textractor.data.constants import LAYOUT_FIGURE
from textractor.parsers import response_parser

from deps_parsing.infrastructure.dl_parsing.document_based_service import (
    DocumentOCRBasedParsingService,
)

from ...proxies import DocumentProxy, FileProxy, UnifiedDataImage, UnifierProxy
from ..image_processing import (
    OCRLayoutImageProcessingService,
    ParsedImage,
    PreparsedImage,
)
from .engine import AWSTextractEngine
from .parser import AWSPage, AWSTextractDocument, AwsTextractParser, StructuredResponse

__all__ = ["AWSTextractDocumentParsingService"]


def _run_with_user_context(executor: ThreadPoolExecutor, func: Callable, *args: Any, **kwargs: Any) -> Future:
    """This method allows us to share user context with threads so we can perform REST API calls"""
    context = copy_context()
    return executor.submit(lambda: context.run(func, *args, **kwargs))


class AWSTextractDocumentParsingService(DocumentOCRBasedParsingService[AWSTextractDocument]):
    parsing_type = ParsingType(ParsingType.AWS_TEXTRACT)
    processable_features = {
        ParsingFeature.TEXT,
        ParsingFeature.KEY_VALUE_PAIRS,
        ParsingFeature.TABLES,
        ParsingFeature.IMAGES,
    }

    def __init__(
        self,
        unifier: UnifierProxy,
        storage: ObjectStorage,
        engine: AWSTextractEngine,
        image_processing_service: OCRLayoutImageProcessingService,
        document: DocumentProxy,
        s3_bucket_name: str,
        parallelism_factor: int,
        file: FileProxy,
    ) -> None:
        super().__init__(
            unifier=unifier,
            storage=storage,
            engine=engine,
            image_processing_service=image_processing_service,
            document=document,
            file=file,
        )
        self._init_aws_storage()
        self._s3_bucket_name = s3_bucket_name
        self._parallelism_factor = parallelism_factor

    def parse(
        self,
        document_layout: DocumentLayout,
        features: set[ParsingFeature],
        language: str | None = None,
    ) -> tuple[DocumentLayout, dict[str, Any]]:
        with self._aws_blob_name(document_layout.id()) as blob_name:
            raw_response = self._engine.recognize_document(
                bucket_name=self._s3_bucket_name,
                key=blob_name,
                features=list(features),
            )
            document = response_parser.parse(raw_response)

            self._extract_images(document=document, document_layout=document_layout, features=features)
            self._update_parsing_features(document_layout, features)

            return document_layout, raw_response

    def add_to_document_layout(
        self,
        document_layout: DocumentLayout,
        parsed_document: AWSTextractDocument,
        parsed_images: list[ParsedImage],
    ) -> None:
        raise NotImplementedError

    def recognize_blob(
        self,
        blob: bytes,
        features: set[ParsingFeature],
        language: str | None = None,
    ) -> AWSTextractDocument:
        raise NotImplementedError

    def _extract_images(
        self,
        document: AWSTextractDocument,
        document_layout: DocumentLayout,
        features: set[ParsingFeature],
    ) -> None:
        awspage_by_pagenum = {page.page_num: page for page in document.pages}
        images = list(self._unifier.get_original_images(document_id=document_layout.id()))

        def process_image(  # noqa: WPS430
            unified_image: UnifiedDataImage,
            parsing_features: set[ParsingFeature],
        ) -> tuple[UnifiedDataImage, list[ParsedImage], AWSPage] | None:
            awspage = awspage_by_pagenum.get(unified_image.page)
            if awspage is None:
                return None

            if ParsingFeature.IMAGES not in parsing_features:
                return unified_image, [], awspage

            self._logger.info(f"Downloading blob {unified_image.blob_name}")
            blob = self._storage.download(path=unified_image.blob_name)
            page_images = self._parse_images_with_page(
                layout_id=document_layout.id(),
                raw_page=blob,
                aws_page=awspage,
            )
            return unified_image, page_images, awspage

        with ThreadPoolExecutor(max_workers=self._parallelism_factor) as executor:
            futures: list[Future] = [_run_with_user_context(executor, process_image, img, features) for img in images]

            for future in futures:
                result = future.result()
                if result is None:
                    continue

                image, parsed_page_images, aws_page = result
                self._add_page_to_document_layout(
                    document_layout=document_layout,
                    image=image,
                    parsed_page_images=parsed_page_images,
                    aws_page=aws_page,
                )

    def _parse_images_with_page(
        self,
        layout_id: str,
        raw_page: bytes,
        aws_page: AWSPage,
    ) -> list[ParsedImage]:
        preparsed_images = [
            PreparsedImage(
                layout_id=layout_id,
                page_image=raw_page,
                polygon=StructuredResponse.polygon_of(layout),
            )
            for layout in aws_page.layouts
            if layout.layout_type == LAYOUT_FIGURE
        ]

        self._logger.info(f"Page {aws_page.page_num} preparsed images amount: {len(preparsed_images)}")

        return self._image_processing_service.process_preparsed_images(
            preparsed_images=preparsed_images,
        )

    def _add_page_to_document_layout(
        self,
        document_layout: DocumentLayout,
        image: UnifiedDataImage,
        parsed_page_images: list[ParsedImage],
        aws_page: AWSPage,
    ) -> None:
        self._logger.info(f"Adding page {aws_page.page_num} to document layout")
        AwsTextractParser(aws_page, image, parsed_page_images).add_page_to(document_layout)

    def _list_preparsed_images(
        self,
        layout_id: str,
        raw_document: bytes,
        parsed_document: AWSTextractDocument,
    ) -> list[PreparsedImage]:
        # might be implemented in the future if needed
        raise NotImplementedError

    def _init_aws_storage(self) -> None:
        self.object_storage_settings = Settings()
        if self.object_storage_settings.type == "aws":
            self._aws_object_storage = self._storage
        else:
            self._aws_object_storage = make_aws_object_storage(self.object_storage_settings.mode)

    @contextmanager
    def _aws_blob_name(self, document_id: str) -> Generator[str, None, None]:
        document_detail = self._document.get_brief_document_info(document_id)

        uploaded = False
        if self.object_storage_settings.type == "aws":
            blob_name = self._get_blob_name(document_detail)
        else:
            document_content = self._document.get_document_files(document_id)
            blob_name = self._aws_object_storage.upload(
                path=document_detail["title"],
                content=document_content,
                replace_if_exists=True,
            )
            uploaded = True

        try:
            yield blob_name
        finally:
            if uploaded:
                self._aws_object_storage.delete(blob_name)
