import pytest
from deps_document_layout.model import Page, ParsingFeature, ParsingType

from deps_parsing.infrastructure.exceptions import (
    DocumentProxyRequestError,
    EntityNotFoundError,
    FileProxyRequestError,
)


@pytest.mark.azure_parsing
def test_parse__by_page__ok(
    unifier_mock,
    storage_mock,
    azure_engine_mock,
    document_layout,
    azure_page_parsing_service,
    azure_analyze_result_page1,
    unified_data_image_page1,
):
    features = {ParsingFeature.TABLES, ParsingFeature.TEXT, ParsingFeature.KEY_VALUE_PAIRS}
    unifier_mock.get_original_images.return_value = [unified_data_image_page1]
    storage_mock.download.return_value = b"File content"
    azure_engine_mock.recognize_blob.return_value = azure_analyze_result_page1
    azure_engine_mock.fetch_received_features.return_value = features

    assert len(document_layout.pages) == 0
    assert document_layout.parsing_features == {}

    document_layout, raw_document_layout = azure_page_parsing_service.parse(document_layout, features)

    assert len(raw_document_layout) == 1
    assert len(document_layout.pages) == 1
    assert isinstance(document_layout.pages[0], Page)
    assert document_layout.parsing_features == {ParsingType.AZURE_FORM_RECOGNIZER: features}


@pytest.mark.azure_parsing
def test_choose_processable_features__only_unprocessable_features__empty_set(azure_page_parsing_service):
    features = {ParsingFeature.IMAGES}

    result = azure_page_parsing_service.choose_processable_features(features)

    assert result == set()


@pytest.mark.azure_parsing
def test_choose_processable_features__all_features__only_processable_features(azure_page_parsing_service):
    features = {ParsingFeature.TABLES, ParsingFeature.TEXT, ParsingFeature.KEY_VALUE_PAIRS, ParsingFeature.IMAGES}
    expected_features = {ParsingFeature.TABLES, ParsingFeature.TEXT, ParsingFeature.KEY_VALUE_PAIRS}

    result = azure_page_parsing_service.choose_processable_features(features)

    assert result == expected_features


@pytest.mark.azure_parsing
def test_parse__by_document__ok(
    unifier_mock,
    document_mock,
    azure_engine_mock,
    document_layout,
    azure_document_parsing_service,
    azure_analyze_result_two_pages,
    unified_data_image_page1,
    unified_data_image_page2,
):
    features = {ParsingFeature.TABLES, ParsingFeature.TEXT, ParsingFeature.KEY_VALUE_PAIRS}
    unifier_mock.get_original_images.return_value = [unified_data_image_page1, unified_data_image_page2]
    document_mock.get_document_files.return_value = b"Document content"
    azure_engine_mock.recognize_blob.return_value = azure_analyze_result_two_pages
    azure_engine_mock.fetch_received_features.return_value = features

    assert len(document_layout.pages) == 0
    assert document_layout.parsing_features == {}

    document_layout, raw_document_layout = azure_document_parsing_service.parse(document_layout, features)

    assert isinstance(raw_document_layout, dict)
    assert len(raw_document_layout["pages"]) == 2
    assert len(document_layout.pages) == 2
    assert isinstance(document_layout.pages[0], Page)
    assert isinstance(document_layout.pages[1], Page)
    assert document_layout.parsing_features == {ParsingType.AZURE_FORM_RECOGNIZER: features}


@pytest.mark.azure_parsing
def test_parse__by_document__fetches_from_document_service(
    unifier_mock,
    document_mock,
    file_mock,
    azure_engine_mock,
    document_layout,
    azure_document_parsing_service,
    azure_analyze_result_two_pages,
    unified_data_image_page1,
    unified_data_image_page2,
):
    features = {ParsingFeature.TEXT}
    unifier_mock.get_original_images.return_value = [unified_data_image_page1, unified_data_image_page2]
    document_mock.get_document_files.return_value = b"Document content"
    file_mock.get_file_content.side_effect = FileProxyRequestError("404 Not Found")
    azure_engine_mock.recognize_blob.return_value = azure_analyze_result_two_pages
    azure_engine_mock.fetch_received_features.return_value = features

    document_layout, _ = azure_document_parsing_service.parse(document_layout, features)

    assert len(document_layout.pages) == 2
    document_mock.get_document_files.assert_called_once()
    azure_engine_mock.recognize_blob.assert_called_once_with(b"Document content", features)


@pytest.mark.azure_parsing
def test_parse__by_document__fetches_from_file_service(
    unifier_mock,
    document_mock,
    file_mock,
    azure_engine_mock,
    document_layout,
    azure_document_parsing_service,
    azure_analyze_result_two_pages,
    unified_data_image_page1,
    unified_data_image_page2,
):
    features = {ParsingFeature.TEXT}
    unifier_mock.get_original_images.return_value = [unified_data_image_page1, unified_data_image_page2]
    document_mock.get_document_files.side_effect = DocumentProxyRequestError("404 Not Found")
    file_mock.get_file_content.return_value = b"File content"
    azure_engine_mock.recognize_blob.return_value = azure_analyze_result_two_pages
    azure_engine_mock.fetch_received_features.return_value = features

    document_layout, _ = azure_document_parsing_service.parse(document_layout, features)

    assert len(document_layout.pages) == 2
    file_mock.get_file_content.assert_called_once()
    azure_engine_mock.recognize_blob.assert_called_once_with(b"File content", features)


@pytest.mark.azure_parsing
def test_parse__by_document__both_services_fail(
    unifier_mock,
    document_mock,
    file_mock,
    azure_engine_mock,
    document_layout,
    azure_document_parsing_service,
    unified_data_image_page1,
):
    features = {ParsingFeature.TEXT}
    unifier_mock.get_original_images.return_value = [unified_data_image_page1]
    document_mock.get_document_files.side_effect = DocumentProxyRequestError("404 Not Found")
    file_mock.get_file_content.side_effect = FileProxyRequestError("404 Not Found")

    with pytest.raises(EntityNotFoundError) as exc_info:
        azure_document_parsing_service.parse(document_layout, features)

    error_message = str(exc_info.value)
    assert document_layout.id() in error_message
