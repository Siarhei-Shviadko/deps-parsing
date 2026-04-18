import pytest
from azure.ai.formrecognizer import (
    DocumentKeyValuePair,
    DocumentLine,
    DocumentPage,
    DocumentParagraph,
    DocumentTable,
    DocumentWord,
)
from deps_document_layout.model import (
    LineBuilder,
    PageBuilder,
    ParagraphBuilder,
    TableBuilder,
    WordBuilder,
)

from deps_parsing.infrastructure.dl_parsing import (
    AzureDocumentParsingService,
    AzurePageParsingService,
)
from deps_parsing.infrastructure.dl_parsing.azure.parser import AzureParser
from deps_parsing.infrastructure.dl_parsing.azure.structured_response import (
    StructuredResponse,
)

FIRST_ELEMENT: int = 0
LAST_ELEMENT: int = -1


@pytest.fixture
def azure_page1(azure_analyze_result_page1) -> DocumentPage:
    return azure_analyze_result_page1.pages[FIRST_ELEMENT]


@pytest.fixture
def page_builder(document_layout) -> PageBuilder:
    return document_layout.add_page()


@pytest.fixture
def table_builder(page_builder) -> TableBuilder:
    return page_builder.with_table()


@pytest.fixture
def paragraph_builder(page_builder) -> ParagraphBuilder:
    return page_builder.with_paragraph()


@pytest.fixture
def line_builder(paragraph_builder) -> LineBuilder:
    return paragraph_builder.with_line()


@pytest.fixture
def word_builder(line_builder) -> WordBuilder:
    return line_builder.with_word()


@pytest.fixture
def structured_response(azure_analyze_result_page1, unified_data_image_page1) -> StructuredResponse:
    return StructuredResponse(azure_analyze_result_page1, [unified_data_image_page1])


@pytest.fixture
def azure_page_parsing_service(parsing_service_mapper, structured_response) -> AzurePageParsingService:
    return parsing_service_mapper.kwargs["AZURE_FORM_RECOGNIZER"]()


@pytest.fixture
def azure_document_parsing_service(parsing_service_mapper, structured_response) -> AzureDocumentParsingService:
    return parsing_service_mapper.kwargs["AZURE_FORM_RECOGNIZER"].by_document()


@pytest.fixture
def azure_parser(document_layout, azure_analyze_result_page1, unified_data_image_page1):
    parser = AzureParser(azure_analyze_result_page1, [unified_data_image_page1])

    return parser


@pytest.fixture
def azure_table(azure_analyze_result_page1) -> DocumentTable:
    return azure_analyze_result_page1.tables[LAST_ELEMENT]


@pytest.fixture
def azure_key_value_pairs(azure_analyze_result_page1) -> list[DocumentKeyValuePair]:
    return azure_analyze_result_page1.key_value_pairs


@pytest.fixture
def azure_paragraph(azure_analyze_result_page1) -> DocumentParagraph:
    return azure_analyze_result_page1.paragraphs[FIRST_ELEMENT]


@pytest.fixture
def azure_line(azure_page1) -> DocumentLine:
    return azure_page1.lines[FIRST_ELEMENT]


@pytest.fixture
def azure_word(structured_response, azure_line) -> DocumentWord:
    return structured_response.pages[0].words_of(azure_line)[LAST_ELEMENT]
