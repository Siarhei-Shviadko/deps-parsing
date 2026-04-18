import pytest

from deps_parsing.infrastructure.dl_parsing import DOCXParsingService
from tests.fakes import FakeDocumentProxy


@pytest.fixture(
    params=[
        ("with_paragraph_and_merged_tables.docx", 71, 2),
        ("with_paragraph_and_table.docx", 52, 1),
        ("with_styled_paragraphs.docx", 4, 0),
        ("with_tables.docx", 54, 3),
    ]
)
def test_docx_documents(request):
    file_name, paragraph_count, table_count = request.param
    with open(f"./tests/data/docx/{file_name}", "rb") as docx_file:
        return docx_file.read(), paragraph_count, table_count


@pytest.fixture
def mocked_service(
    fake_document_proxy: FakeDocumentProxy,
    docx_file_with_paragraph_and_table: bytes,
):
    fake_document_proxy.set_mocked_file(docx_file_with_paragraph_and_table)

    return DOCXParsingService(documents_proxy=fake_document_proxy)
