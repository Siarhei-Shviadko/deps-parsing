import json
from http import HTTPStatus

import pytest
from deps_document_layout.model import ParsingType
from deps_object_storage import FileNotFound, ObjectStorageException

from tests.fakes import FakeResponse


def test_save_raw_document_layout__ok(raw_document_layout_repository, test_document_layout_dict):
    test_file_path = "test_file_path/example.json"
    raw_document_layout_repository._object_storage._session.post.return_value = FakeResponse(
        status_code=HTTPStatus.OK, content=json.dumps({"path": test_file_path})
    )
    response = raw_document_layout_repository.save("example", test_document_layout_dict, ParsingType.TESSERACT)

    assert response == test_file_path


def test_save_raw_document_layout__request_failed__error(raw_document_layout_repository, test_document_layout_dict):
    raw_document_layout_repository._object_storage._session.post.return_value = FakeResponse(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR, content=b'{"message": "I will be back"}'
    )
    with pytest.raises(ObjectStorageException):
        raw_document_layout_repository.save("example", test_document_layout_dict, ParsingType.TESSERACT)


def test_layout_of_document_id__ok(raw_document_layout_repository, test_document_layout_dict):
    raw_document_layout_repository._object_storage._session.get.return_value = FakeResponse(
        status_code=HTTPStatus.OK, content=json.dumps(test_document_layout_dict)
    )
    raw_layout = raw_document_layout_repository.layout_of_id("example", ParsingType.TESSERACT)

    assert raw_layout == test_document_layout_dict


def test_layout_of_document_id__not_existing_layout__error(raw_document_layout_repository, test_document_layout_dict):
    raw_document_layout_repository._object_storage._session.get.return_value = FakeResponse(
        status_code=HTTPStatus.NOT_FOUND,
        content=json.dumps(
            {"code": "not_found_exception", "message": "Could not find the file 'document_layout/3.json'"}
        ),
    )
    with pytest.raises(FileNotFound):
        raw_document_layout_repository.layout_of_id("fake_document_id", ParsingType.TESSERACT)
