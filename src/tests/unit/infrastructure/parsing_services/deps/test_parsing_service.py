import pytest
from deps_document_layout.model import (
    DocumentLayoutFeaturesFilter,
    ParsingFeature,
    ParsingType,
)

from tests.data.deps import ocr_response_, tables_response_


@pytest.mark.parametrize(
    "parsing_type",
    [ParsingType.TESSERACT, ParsingType.CRAFT_TESSERACT, ParsingType.EASYOCR, ParsingType.PADDLEOCR],
)
def test_deps_parsing_service(
    tesseract_engine_mock,
    easy_ocr_engine_mock,
    craft_tesseract_engine_mock,
    paddle_ocr_engine_mock,
    unifier_mock,
    unified_data_image_page1,
    parsing_type,
    storage_mock,
    document_layout_repository_mock,
    document_layout_service,
    tenant_id,
):
    valid_fixture = {
        ParsingType.TESSERACT: tesseract_engine_mock,
        ParsingType.CRAFT_TESSERACT: craft_tesseract_engine_mock,
        ParsingType.EASYOCR: easy_ocr_engine_mock,
        ParsingType.PADDLEOCR: paddle_ocr_engine_mock,
    }
    deps_engine_mock = valid_fixture[parsing_type]

    unifier_mock.get_original_images.return_value = [unified_data_image_page1]
    storage_mock.download.return_value = b"File content"
    deps_engine_mock.recognize_blob.return_value = {"ocr_data": ocr_response_, "tables_data": tables_response_}
    document_layout_repository_mock.layout_of_id.return_value = None
    deps_engine_mock.fetch_received_features.return_value = {ParsingFeature.TEXT, ParsingFeature.TABLES}

    layout = document_layout_service.get_or_create_document_layout(
        document_layout_id="abc",
        tenant_id=tenant_id,
        filtering=DocumentLayoutFeaturesFilter(
            parsing_type=parsing_type, features={ParsingFeature.TABLES, ParsingFeature.TEXT}
        ),
        language="eng",
    )

    assert layout.pages[0].paragraphs
    assert layout.pages[0].tables
    assert not layout.pages[0].key_value_pairs
    assert not layout.pages[0].images
