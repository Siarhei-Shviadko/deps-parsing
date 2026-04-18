from typing import Generator

import pytest

from deps_parsing.containers import Containers
from deps_parsing.infrastructure import UnifiedDataImage
from deps_parsing.infrastructure.dl_parsing import (
    DocumentAIPageParsingService,
    OCRLayoutImageProcessingService,
)
from deps_parsing.infrastructure.dl_parsing.google.document_service import (
    DocumentAIDocumentParsingService,
)
from deps_parsing.infrastructure.dl_parsing.google.engine import DocumentAIEngine
from deps_parsing.infrastructure.dl_parsing.google.parser import DocAIDocument
from tests.fakes import FakeDocumentAIProxy


def _parse_file(filename) -> DocAIDocument:
    with open(filename, "r") as file:
        raw_data: str = file.read()

    return DocAIDocument.from_json(raw_data)  # type: ignore


@pytest.fixture
def parsed_file__all_types() -> DocAIDocument:
    return _parse_file("tests/data/google/raw-form-recognition-response-easy-to-validate.json")


@pytest.fixture
def fake_docai_proxy(containers: Containers) -> Generator[FakeDocumentAIProxy, None, None]:
    with containers.external_services.gcp_document_ai.override(FakeDocumentAIProxy()):
        yield containers.external_services.gcp_document_ai()


@pytest.fixture
def docai_engine(fake_docai_proxy: FakeDocumentAIProxy, containers: Containers) -> DocumentAIEngine:
    return containers.engines.document_ai()


@pytest.fixture
def fake_docai_proxy_with_mocked_file_response(
    fake_docai_proxy: FakeDocumentAIProxy,
    parsed_file__all_types: DocAIDocument,
) -> FakeDocumentAIProxy:
    fake_docai_proxy.response = parsed_file__all_types

    return fake_docai_proxy


@pytest.fixture
def mocked_document_ai_parsing_service(
    unifier_mock,
    storage_mock,
    ai_fusion_mock,
    fake_docai_proxy_with_mocked_file_response: FakeDocumentAIProxy,
    docai_engine: DocumentAIEngine,
    unified_data_image_page1: UnifiedDataImage,
    ocr_image_processing_service: OCRLayoutImageProcessingService,
) -> DocumentAIPageParsingService:
    unifier_mock.get_original_images.return_value = [unified_data_image_page1]
    storage_mock.download.return_value = b"blob"
    return DocumentAIPageParsingService(
        unifier=unifier_mock,
        storage=storage_mock,
        engine=docai_engine,
        image_processing_service=ocr_image_processing_service,
    )


@pytest.fixture
def mocked_document_ai_document_parsing_service(
    mocker,
    unifier_mock,
    storage_mock,
    document_mock,
    file_mock,
    fake_docai_proxy_with_mocked_file_response: FakeDocumentAIProxy,
    docai_engine: DocumentAIEngine,
    unified_data_image_page1: UnifiedDataImage,
    unified_data_image_page2: UnifiedDataImage,
    ocr_image_processing_service: OCRLayoutImageProcessingService,
) -> DocumentAIDocumentParsingService:
    unifier_mock.get_original_images.return_value = [unified_data_image_page1]
    storage_mock.download.return_value = b"File content"
    storage_mock.upload.return_value = "test_blob.pdf"
    document_mock.get_brief_document_info.return_value = {"id": "123", "files": "test_blob.pdf", "title": "test.pdf"}

    mocker.patch(
        "deps_parsing.infrastructure.dl_parsing.google.document_service.make_gcp_object_storage",
        return_value=storage_mock,
    )

    return DocumentAIDocumentParsingService(
        unifier=unifier_mock,
        storage=storage_mock,
        engine=docai_engine,
        image_processing_service=ocr_image_processing_service,
        document=document_mock,
        file=file_mock,
        output_directory="gs://bucket/output/",
    )
