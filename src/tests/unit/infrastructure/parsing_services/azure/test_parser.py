import pytest
from deps_document_layout.model import (
    Barcode,
    Cell,
    Dimension,
    Formula,
    KeyValuePair,
    KeyValuePairElement,
    Language,
    Line,
    Page,
    Paragraph,
    SelectionMark,
    Style,
    Table,
    Transformations,
    Word,
)

from deps_parsing.infrastructure.dl_parsing.azure.checkmarks import AzureCheckmarksMap
from deps_parsing.infrastructure.dl_parsing.azure.parser import AzureParser
from deps_parsing.infrastructure.exceptions import PageCountMismatchError

FIRST_ELEMENT: int = 0
LAST_ELEMENT: int = -1


@pytest.mark.azure_parsing
def test_add_page__ok(
    azure_parser,
    document_layout,
    azure_analyze_result_page1,
    unified_data_image_page1,
    azure_page1,
):
    expected_page = azure_parser._response.pages[0]
    page_builder = azure_parser._add_page(document_layout, expected_page)

    page = page_builder.build()
    assert isinstance(page, Page)
    assert page.id() == unified_data_image_page1.id
    assert page.page_number == unified_data_image_page1.page
    assert page.file_path == unified_data_image_page1.blob_name
    assert page.dimension == Dimension(int(azure_page1.width), int(azure_page1.height), azure_page1.unit)
    assert page.parsing_type == azure_parser.parsing_type
    assert page.transformations == Transformations(angle=azure_page1.angle)
    assert page.languages == tuple(
        Language(lang.locale, lang.confidence) for lang in azure_analyze_result_page1.languages
    )


@pytest.mark.azure_parsing
def test_add_tables__ok(azure_parser, structured_response, page_builder, azure_table):
    expected_page = azure_parser._response.pages[0]
    cell_builder = azure_parser._add_tables(page_builder, expected_page)

    table = cell_builder._parent._build()
    polygon = expected_page.convert_bounding_region_to_polygon(
        azure_table.bounding_regions[FIRST_ELEMENT],
    )

    assert isinstance(table, Table)
    assert isinstance(table.order, int)
    assert table.row_count == azure_table.row_count
    assert table.column_count == azure_table.column_count
    assert table.polygon == polygon
    assert table.confidence is None
    assert table.cells
    assert isinstance(table.cells[FIRST_ELEMENT], Cell)


@pytest.mark.azure_parsing
def test_add_cells__ok(azure_parser, structured_response, table_builder, azure_table):
    expected_page = azure_parser._response.pages[0]
    cell_builder = azure_parser._add_cells(azure_table, table_builder, expected_page)

    cell = cell_builder._build()
    azure_cell = azure_table.cells[LAST_ELEMENT]
    polygon = expected_page.convert_bounding_region_to_polygon(
        azure_cell.bounding_regions[FIRST_ELEMENT],
    )

    assert cell.content == azure_cell.content
    assert cell.polygon == polygon
    assert cell.kind == azure_cell.kind
    assert cell.row_span == azure_cell.row_span
    assert cell.row_index == azure_cell.row_index
    assert cell.column_span == azure_cell.column_span
    assert cell.column_index == azure_cell.column_index


@pytest.mark.azure_parsing
def test_add_key_value_pairs__with_value__ok(azure_parser, page_builder, azure_key_value_pairs):
    expected_page = azure_parser._response.pages[0]
    element_builder = azure_parser._add_key_value_pairs(page_builder, expected_page)

    key_value_pair = element_builder._parent._parent._key_value_pairs[FIRST_ELEMENT]
    azure_key_value_pair = azure_key_value_pairs[FIRST_ELEMENT]

    assert isinstance(key_value_pair, KeyValuePair)
    assert isinstance(key_value_pair.order, int)
    assert key_value_pair.confidence == azure_key_value_pair.confidence
    assert isinstance(key_value_pair.value, KeyValuePairElement)
    assert isinstance(key_value_pair.key, KeyValuePairElement)


@pytest.mark.azure_parsing
def test_add_key_value_pairs_with_checkmark__ok(azure_parser, page_builder, azure_key_value_pairs):
    expected_page = azure_parser._response.pages[0]
    element_builder = azure_parser._add_key_value_pairs(page_builder, expected_page)

    key_value_pair = element_builder._parent._parent._key_value_pairs[FIRST_ELEMENT]
    azure_key_value_pair = azure_key_value_pairs[FIRST_ELEMENT]

    assert isinstance(key_value_pair, KeyValuePair)
    assert isinstance(key_value_pair.order, int)
    assert key_value_pair.confidence == azure_key_value_pair.confidence

    if key_value_pair.value.content in AzureCheckmarksMap:
        assert key_value_pair.value.content in AzureCheckmarksMap.values()

    assert isinstance(key_value_pair.value, KeyValuePairElement)
    assert isinstance(key_value_pair.key, KeyValuePairElement)


@pytest.mark.azure_parsing
def test_add_key_value_pairs__without_value__ok(
    azure_parser,
    structured_response,
    page_builder,
    azure_key_value_pairs,
):
    expected_page = azure_parser._response.pages[0]
    element_builder = azure_parser._add_key_value_pairs(page_builder, expected_page)

    key_value_pair = element_builder._parent._parent._key_value_pairs[9]
    azure_key_value_pair = azure_key_value_pairs[9]
    polygon = expected_page.convert_bounding_region_to_polygon(
        azure_key_value_pair.key.bounding_regions[FIRST_ELEMENT],
    )

    assert key_value_pair.confidence == azure_key_value_pair.confidence
    assert key_value_pair.value is None
    assert key_value_pair.key.polygon == polygon
    assert key_value_pair.key.content == azure_key_value_pair.key.content


@pytest.mark.azure_parsing
def test_add_paragraphs__ok(azure_parser, structured_response, page_builder, azure_paragraph):
    expected_page = azure_parser._response.pages[0]
    word_builder = azure_parser._add_paragraphs(page_builder, expected_page)

    paragraph = word_builder._parent._parent._parent._paragraphs[FIRST_ELEMENT]
    polygon = expected_page.convert_bounding_region_to_polygon(
        azure_paragraph.bounding_regions[FIRST_ELEMENT],
    )

    assert isinstance(paragraph, Paragraph)
    assert paragraph.content == azure_paragraph.content
    assert paragraph.polygon == polygon
    assert paragraph.role == azure_paragraph.role
    assert isinstance(paragraph.order, int)
    assert isinstance(paragraph.lines[FIRST_ELEMENT], Line)


@pytest.mark.azure_parsing
def test_add_lines__ok(azure_parser, structured_response, paragraph_builder, azure_paragraph):
    expected_page = azure_parser._response.pages[0]
    word_builder = azure_parser._add_lines(paragraph_builder, azure_paragraph, expected_page)

    line = word_builder._parent._parent._lines[FIRST_ELEMENT]
    azure_line = expected_page.lines_of(azure_paragraph)[FIRST_ELEMENT]
    polygon = expected_page.convert_abs_coordinates_to_relative(azure_line.polygon)

    assert isinstance(line, Line)
    assert isinstance(line.order, int)
    assert line.content == azure_line.content
    assert line.polygon == polygon
    assert isinstance(line.words[FIRST_ELEMENT], Word)
    assert isinstance(line.selection_marks[FIRST_ELEMENT], SelectionMark)
    assert isinstance(line.barcodes[FIRST_ELEMENT], Barcode)
    assert isinstance(line.formulas[FIRST_ELEMENT], Formula)


@pytest.mark.azure_parsing
def test_add_words__without_style__ok(azure_parser, structured_response, azure_line, line_builder):
    expected_page = azure_parser._response.pages[0]
    word_builder = azure_parser._add_words(azure_line, line_builder, expected_page)

    word = word_builder._parent._words[FIRST_ELEMENT]
    azure_word = expected_page.words_of(azure_line)[FIRST_ELEMENT]
    polygon = expected_page.convert_abs_coordinates_to_relative(azure_word.polygon)

    assert isinstance(word, Word)
    assert isinstance(word.order, int)
    assert word.content == azure_word.content
    assert word.confidence == azure_word.confidence
    assert word.polygon == polygon
    assert word.style == Style()


@pytest.mark.azure_parsing
def test_add_style__ok(azure_parser, structured_response, azure_word, word_builder):
    word_builder = azure_parser._add_style(
        azure_word,
        word_builder,
    )

    style = word_builder._style
    azure_style = structured_response.style_of(azure_word)

    assert isinstance(style, Style)
    assert style.background_color == azure_style.background_color
    assert style.color == azure_style.color
    assert style.bold == (azure_style.font_weight == "bold")
    assert style.italic == (azure_style.font_style == "italic")
    assert style.font_type == azure_style.similar_font_family
    assert style.handwritten == azure_style.is_handwritten


@pytest.mark.azure_parsing
def test_add_selection_marks__ok(azure_parser, structured_response, azure_line, line_builder):
    expected_page = azure_parser._response.pages[0]
    selection_mark_builder = azure_parser._add_selection_marks(azure_line, line_builder, expected_page)

    selection_mark = selection_mark_builder._build()
    azure_selection_mark = expected_page.selection_marks_of(azure_line)[FIRST_ELEMENT]
    polygon = expected_page.convert_abs_coordinates_to_relative(azure_selection_mark.polygon)

    assert isinstance(selection_mark, SelectionMark)
    assert isinstance(selection_mark.order, int)
    assert selection_mark.state == azure_selection_mark.state
    assert selection_mark.confidence == azure_selection_mark.confidence
    assert selection_mark.polygon == polygon


@pytest.mark.azure_parsing
def test_add_barcodes__ok(azure_parser, structured_response, azure_line, line_builder):
    expected_page = azure_parser._response.pages[0]
    barcode_builder = azure_parser._add_barcodes(azure_line, line_builder, expected_page)

    barcode = barcode_builder._build()
    azure_barcode = expected_page.barcodes_of(azure_line)[FIRST_ELEMENT]
    polygon = expected_page.convert_abs_coordinates_to_relative(azure_barcode.polygon)

    assert isinstance(barcode, Barcode)
    assert isinstance(barcode.order, int)
    assert barcode.kind == azure_barcode.kind
    assert barcode.value == azure_barcode.value
    assert barcode.confidence == azure_barcode.confidence
    assert barcode.polygon == polygon


@pytest.mark.azure_parsing
def test_add_formulas__ok(azure_parser, structured_response, azure_line, line_builder):
    expected_page = azure_parser._response.pages[0]
    formula_builder = azure_parser._add_formulas(azure_line, line_builder, expected_page)

    formula = formula_builder._build()
    azure_formula = expected_page.formulas_of(azure_line)[FIRST_ELEMENT]
    polygon = expected_page.convert_abs_coordinates_to_relative(azure_formula.polygon)

    assert isinstance(formula, Formula)
    assert isinstance(formula.order, int)
    assert formula.kind == azure_formula.kind
    assert formula.value == azure_formula.value
    assert formula.confidence == azure_formula.confidence
    assert formula.polygon == polygon


@pytest.mark.azure_parsing
def test_add_different_number_of_pages_and_images__error(
    azure_analyze_result_page1,
    unified_data_image_page1,
    unified_data_image_page2,
):
    with pytest.raises(PageCountMismatchError):
        AzureParser(azure_analyze_result_page1, [unified_data_image_page2, unified_data_image_page1])


@pytest.mark.azure_parsing
def test_add_page_by_page_no_errors(
    document_layout,
    azure_analyze_result_page1,
    azure_analyze_result_page2,
    unified_data_image_page1,
    unified_data_image_page2,
):
    AzureParser(azure_analyze_result_page1, [unified_data_image_page1]).add_pages_to(document_layout)
    AzureParser(azure_analyze_result_page2, [unified_data_image_page2]).add_pages_to(document_layout)

    assert len(document_layout.pages) == 2
