import pytest
from deps_document_layout.model import (
    Cell,
    KeyValuePair,
    Page,
    Paragraph,
    ParsingType,
    Table,
    Word,
)

from deps_parsing.domain.model import CheckmarkValue
from deps_parsing.infrastructure.dl_parsing import (
    AWSCell,
    AWSKeyValuePair,
    AWSLayout,
    AWSLine,
    AWSParagraph,
    AWSTable,
    AwsTextractParser,
    AWSWord,
    ChildType,
)


class TestAwsTextractParser:
    @pytest.mark.parametrize(
        "page_parser",
        ["page1_textract_parser", "page2_textract_parser", "page_with_checkbox_inside_table_cell_parser"],
    )
    def test_full_build(self, request, document_layout, page_parser, unified_data_image_page1):
        parser: AwsTextractParser = request.getfixturevalue(page_parser)
        parser.add_page_to(document_layout)
        assert True

    @pytest.mark.parametrize(
        "page_parser",
        ["page1_textract_parser", "page2_textract_parser", "page_with_checkbox_inside_table_cell_parser"],
    )
    def test_add_page__added(self, request, document_layout, page_parser, unified_data_image_page1):
        parser: AwsTextractParser = request.getfixturevalue(page_parser)

        page = parser._add_page(document_layout).build()

        self._compare_pages(page, unified_data_image_page1)

    @pytest.mark.parametrize(
        "page_parser", ["page1_textract_parser", "page2_textract_parser", "page_with_checkbox_inside_table_cell_parser"]
    )
    def test_add_tables__ok(self, document_layout, page_parser, request):
        parser: AwsTextractParser = request.getfixturevalue(page_parser)
        input_tables = parser._response.tables
        page_builder = parser._add_page(document_layout)

        page_with_tables = parser._add_tables(page_builder).build()

        assert page_with_tables.tables
        assert len(page_with_tables.tables) == len(input_tables)
        for table, input_table in zip(page_with_tables.tables, input_tables):
            self._compare_tables(table, input_table)

    @pytest.mark.parametrize("page_parser", ["page1_textract_parser", "page2_textract_parser"])
    def test_add_kvps__ok(self, document_layout, request, page_parser):
        parser: AwsTextractParser = request.getfixturevalue(page_parser)
        input_kvps = parser._response.key_value_pairs
        page_builder = parser._add_page(document_layout)

        page_with_kvps = parser._add_key_value_pairs(page_builder).build()

        assert page_with_kvps.key_value_pairs
        assert len(page_with_kvps.key_value_pairs) == len(input_kvps)
        for kvp, input_kvp in zip(page_with_kvps.key_value_pairs, input_kvps):
            self._compare_kvps(kvp, input_kvp)

    @pytest.mark.parametrize("page_parser", ["page1_textract_parser", "page2_textract_parser"])
    def test_add_paragraph__ok(self, document_layout, page_parser, request):
        parser: AwsTextractParser = request.getfixturevalue(page_parser)
        input_paragraphs: list[AWSParagraph] = parser._response.paragraphs
        page_builder = parser._add_page(document_layout)

        page_with_paragraphs = parser._add_paragraphs(page_builder).build()

        assert page_with_paragraphs.paragraphs
        assert len(page_with_paragraphs.paragraphs) == len(input_paragraphs)

        for paragraph, original_paragraph in zip(page_with_paragraphs.paragraphs, input_paragraphs):
            self._compare_children(paragraph, original_paragraph)

    @pytest.mark.parametrize("page_parser", ["page1_textract_parser", "page2_textract_parser"])
    def test_add_checkbox__ok(self, document_layout, page_parser, request):
        parser: AwsTextractParser = request.getfixturevalue(page_parser)
        input_checkboxes: list[AWSLine] = parser._response.checkboxes
        page_builder = parser._add_page(document_layout)
        page_with_checkboxes = parser._add_checkboxes(page_builder).build()

        assert page_with_checkboxes.paragraphs
        assert len(page_with_checkboxes.key_value_pairs) == len(input_checkboxes)

        for kvp, input_kvp in zip(page_with_checkboxes.key_value_pairs, input_checkboxes):
            self._compare_kvps(kvp, input_kvp)

    def test_add_images__ok(self, document_layout, page_with_image_parser, page_with_image_aws_document, parsed_image):
        page_builder = page_with_image_parser._add_page(document_layout)

        page_with_images = page_with_image_parser._add_images(page_builder).build()
        assert len(page_with_images.images) == 1

        image = page_with_images.images[0]

        assert image.file_path == parsed_image.filepath
        assert image.title == parsed_image.title
        assert image.description == parsed_image.description
        assert image.polygon == parsed_image.page_coordinates

    def test_add_paragraphs__nested_layout_children__every_line_has_words(
        self, document_layout, page_with_nested_layout_list_parser
    ):
        page_builder = page_with_nested_layout_list_parser._add_page(document_layout)

        page_with_paragraphs = page_with_nested_layout_list_parser._add_paragraphs(page_builder).build()

        content_bearing_lines = [
            line for paragraph in page_with_paragraphs.paragraphs for line in paragraph.lines if line.content.strip()
        ]
        assert content_bearing_lines
        for line in content_bearing_lines:
            assert line.words

    def test_add_paragraphs__nested_layout_children__flattened_into_lines(
        self, document_layout, page_with_nested_layout_list_parser
    ):
        parser = page_with_nested_layout_list_parser
        input_paragraphs: list[AWSParagraph] = parser._response.paragraphs
        nested_layout_paragraphs = [
            paragraph
            for paragraph in input_paragraphs
            if any(isinstance(child, AWSLayout) for child in paragraph.children)
        ]
        assert nested_layout_paragraphs

        page_builder = parser._add_page(document_layout)
        page_with_paragraphs = parser._add_paragraphs(page_builder).build()

        for paragraph, original_paragraph in zip(page_with_paragraphs.paragraphs, input_paragraphs):
            if not any(isinstance(child, AWSLayout) for child in original_paragraph.children):
                continue
            flattened_lines = self._flatten_paragraph_children(original_paragraph.children)
            assert len(paragraph.lines) == len(flattened_lines)
            assert len(paragraph.lines) > len(original_paragraph.children)

    @staticmethod
    def _compare_pages(page: Page, unified_data_image_page1):
        assert isinstance(page, Page)
        assert page.id() == unified_data_image_page1.id
        assert page.page_number == unified_data_image_page1.page
        assert page.file_path == unified_data_image_page1.blob_name
        assert page.parsing_type == ParsingType.AWS_TEXTRACT
        assert page.languages == ()

    def _compare_tables(self, table: Table, input_table: AWSTable):
        assert table.row_count == input_table.row_count
        assert table.column_count == input_table.column_count
        assert table.confidence is None

        assert len(table.cells) == len(input_table.table_cells)
        for cell, input_cell in zip(table.cells, input_table.table_cells):
            self._compare_cells(cell, input_cell)

    @staticmethod
    def _compare_cells(cell: Cell, input_cell: AWSCell):
        assert cell.row_index == input_cell.row_index - 1
        assert cell.row_span == input_cell.row_span
        assert cell.column_index == input_cell.col_index - 1
        assert cell.column_span == input_cell.col_span
        assert cell.content == input_cell.text

    def _compare_kvps(self, kvp: KeyValuePair, input_kvp: AWSKeyValuePair):
        assert kvp.confidence == input_kvp.confidence
        assert kvp.key.content == " ".join(word.text for word in input_kvp.key)
        assert (
            kvp.value.content == input_kvp.value.get_text()
            if not input_kvp.contains_checkbox
            else CheckmarkValue.CHECKED
            if input_kvp.value.children[0].is_selected()
            else CheckmarkValue.UNCHECKED
        )

    def _compare_children(self, paragraph: Paragraph, input_paragraph: AWSParagraph):
        assert paragraph.content == input_paragraph.layout_object.text
        assert paragraph.confidence == input_paragraph.layout_object.confidence

        flattened_children = self._flatten_paragraph_children(input_paragraph.children)
        assert len(paragraph.lines) == len(flattened_children)

        for line, child in zip(paragraph.lines, flattened_children):
            assert line.content == child.text
            assert line.confidence == child.confidence

            for word, input_word in zip(line.words, child.words):
                self._compare_words(word, input_word)

    @classmethod
    def _flatten_paragraph_children(cls, children: list[ChildType]) -> list[ChildType]:
        flattened: list[ChildType] = []
        for child in children:
            if isinstance(child, AWSLayout):
                flattened.extend(cls._flatten_paragraph_children(child.children))
            else:
                flattened.append(child)
        return flattened

    def _compare_words(self, word: Word, input_word: AWSWord):
        assert word.content == input_word.text
        assert word.confidence == input_word.confidence
