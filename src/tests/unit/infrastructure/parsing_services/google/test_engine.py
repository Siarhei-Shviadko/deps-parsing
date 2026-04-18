import pytest
from deps_document_layout.model import ParsingFeature
from google.cloud.documentai import Document

from deps_parsing.infrastructure.dl_parsing.google.engine import DocumentAIEngine
from tests.fakes import FakeDocumentAIProxy


@pytest.mark.parametrize(
    "filename, expected_mimetype",
    [
        ("some-file.pdf", "application/pdf"),
        ("some-file.png.pdf", "application/pdf"),
        ("some-file.jpg", "image/jpeg"),
        ("some-file.png", "image/png"),
        ("some-file.tif", "image/tiff"),
    ],
)
def test_recognize_blob__blob_is_recognized(
    fake_docai_proxy_with_mocked_file_response: FakeDocumentAIProxy,
    docai_engine: DocumentAIEngine,
    filename: str,
    expected_mimetype: str,
):
    fake_blob = b"fake blob"
    features = {ParsingFeature.TABLES, ParsingFeature.KEY_VALUE_PAIRS}

    response = docai_engine.recognize_blob(fake_blob, features, filename=filename)

    assert isinstance(response, Document)
    assert fake_docai_proxy_with_mocked_file_response.last_called_content == fake_blob
    assert fake_docai_proxy_with_mocked_file_response.last_called_mimetype == expected_mimetype


def test_fetch_received_features__static_all_features(docai_engine: DocumentAIEngine):
    assert docai_engine.fetch_received_features(set()) == {
        ParsingFeature.TABLES,
        ParsingFeature.KEY_VALUE_PAIRS,
        ParsingFeature.TEXT,
    }
