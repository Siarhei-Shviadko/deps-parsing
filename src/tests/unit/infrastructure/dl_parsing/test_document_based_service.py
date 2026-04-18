import pytest

from deps_parsing.infrastructure.exceptions import (
    DocumentProxyRequestError,
    EntityNotFoundError,
    FileProxyRequestError,
)


def test_fetch_blob__document_service_succeeds__returns_document_content(document_based_service_with_mocks):
    service, document_mock, file_mock = document_based_service_with_mocks

    document_mock.get_document_files.return_value = b"document content"
    file_mock.get_file_content.side_effect = FileProxyRequestError("404 Not Found")

    result = service._fetch_blob("doc-123")

    assert result == b"document content"
    document_mock.get_document_files.assert_called_once_with(document_id="doc-123")


def test_fetch_blob__file_service_succeeds__returns_file_content(document_based_service_with_mocks):
    service, document_mock, file_mock = document_based_service_with_mocks

    document_mock.get_document_files.side_effect = DocumentProxyRequestError("404 Not Found")
    file_mock.get_file_content.return_value = b"file content"

    result = service._fetch_blob("file-456")

    assert result == b"file content"
    file_mock.get_file_content.assert_called_once_with(file_id="file-456")


def test_fetch_blob__both_services_fail__raises_entity_not_found(document_based_service_with_mocks):
    service, document_mock, file_mock = document_based_service_with_mocks

    document_mock.get_document_files.side_effect = DocumentProxyRequestError("404 Not Found")
    file_mock.get_file_content.side_effect = FileProxyRequestError("404 Not Found")

    with pytest.raises(EntityNotFoundError) as exc_info:
        service._fetch_blob("invalid-id")

    error_message = str(exc_info.value)
    assert "invalid-id" in error_message
