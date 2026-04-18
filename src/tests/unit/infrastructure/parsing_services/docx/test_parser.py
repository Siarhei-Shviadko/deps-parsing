from io import BytesIO

from deps_document_layout.model import DocumentLayoutFactory
from docx import Document as DocxDocument

from deps_parsing.infrastructure.dl_parsing.docx.parser import DOCXParser


def test_parser__ok(test_docx_documents, document_id, tenant_id):
    docx_document, paragraph_count, table_count = test_docx_documents
    test_document_layout = DocumentLayoutFactory.make_document_layout(tenant_id, document_id)

    with BytesIO(docx_document) as docx_file:
        docx_document = DocxDocument(docx_file)

    DOCXParser(docx_document).add_page_to(test_document_layout)

    assert len(test_document_layout.pages) == 1
    assert len(test_document_layout.pages[0].paragraphs) == paragraph_count
    assert len(test_document_layout.pages[0].tables) == table_count


def test_parser_with_document_data__ok(docx_file_with_paragraph_and_table, document_id, tenant_id):
    test_document_layout = DocumentLayoutFactory.make_document_layout(tenant_id, document_id)

    with BytesIO(docx_file_with_paragraph_and_table) as docx_file:
        docx_document = DocxDocument(docx_file)

    DOCXParser(docx_document).add_page_to(test_document_layout)

    assert len(test_document_layout.pages) == 1

    document_paragraphs = test_document_layout.pages[0].paragraphs
    document_tables = test_document_layout.pages[0].tables

    for paragraph in document_paragraphs:
        assert len(paragraph.lines) == 1

        paragraph_words = [word.content for word in paragraph.lines[0].words]
        if paragraph_words:
            assert paragraph.content == " ".join(paragraph_words)

    for table in document_tables:
        assert len(table.cells) <= table.column_count * table.row_count
