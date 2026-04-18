import pytest

from tests.shared_document_layout_fixtures.document_layout_for_db import *


@pytest.fixture
def save_document_layout(document_layout_repository, document_layout) -> None:
    document_layout_repository.save(document_layout)
