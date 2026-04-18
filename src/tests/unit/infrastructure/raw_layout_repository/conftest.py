import pytest
from requests import Session


@pytest.fixture
def mock_file_storage_proxy(containers, mocker):
    object_storage = containers.external_services.object_storage()
    object_storage._session = mocker.Mock(spec=Session)
    yield object_storage


@pytest.fixture
def raw_document_layout_repository(repositories, mock_file_storage_proxy):
    return repositories.raw_document_layout()
