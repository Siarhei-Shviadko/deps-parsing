import pytest

from tests.fakes import FakeDocumentOCRParsingService


@pytest.fixture
def document_based_service_with_mocks(
    unifier_mock,
    storage_mock,
    azure_engine_mock,
    ocr_image_processing_service,
    document_mock,
    file_mock,
):
    service = FakeDocumentOCRParsingService(
        unifier=unifier_mock,
        storage=storage_mock,
        engine=azure_engine_mock,
        image_processing_service=ocr_image_processing_service,
        document=document_mock,
        file=file_mock,
    )

    return service, document_mock, file_mock


@pytest.fixture
def document_based_service_without_file_proxy(
    unifier_mock,
    storage_mock,
    azure_engine_mock,
    ocr_image_processing_service,
    document_mock,
):
    service = FakeDocumentOCRParsingService(
        unifier=unifier_mock,
        storage=storage_mock,
        engine=azure_engine_mock,
        image_processing_service=ocr_image_processing_service,
        document=document_mock,
        file=None,
    )

    return service, document_mock
