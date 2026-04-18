from azure.ai.formrecognizer import (
    AnalyzeResult,
    DocumentKeyValueElement,
    DocumentLine,
    DocumentParagraph,
    DocumentTable,
    DocumentWord,
)
from deps_document_layout.model import (
    CellBuilder,
    DocumentLayout,
    KeyValuePairElementBuilder,
    LineBuilder,
    PageBuilder,
    ParagraphBuilder,
    ParsingType,
    TableBuilder,
    WordBuilder,
)

from ...proxies import UnifiedDataImage
from .structured_response import StructuredPage, StructuredResponse
from .value_response import ValueResponse

__all__ = ["AzureParser"]

FIRST_ELEMENT: int = 0


class AzureParser:
    parsing_type = ParsingType.AZURE_FORM_RECOGNIZER

    def __init__(self, response: AnalyzeResult, images: list[UnifiedDataImage]) -> None:
        self._response = StructuredResponse(parsed_result=response, images=images)

    def add_pages_to(self, document_layout: DocumentLayout) -> DocumentLayout:
        for page in self._response.pages:
            page_builder = self._add_page(document_layout, page)
            page_builder = self._add_tables(page_builder, page)
            page_builder = self._add_key_value_pairs(page_builder, page)
            page_builder = self._add_paragraphs(page_builder, page)
            page_builder.build()

        return document_layout

    def _add_page(self, document_layout: DocumentLayout, page: StructuredPage) -> PageBuilder:
        builder = (
            document_layout.add_page()
            .with_id(page.source_id)
            .with_page_number(page.page_number)
            .with_parsing_type(self.parsing_type)
            .with_dimension(
                width=int(page.width),
                height=int(page.height),
                unit=page.unit,
            )
            .with_file_path(page.file_path)
            .with_transformations()
            .with_angle(page.angle)
        )

        for language in page.languages:
            builder = builder.with_language(language.locale, language.confidence)

        return builder

    def _add_tables(self, builder: PageBuilder, page: StructuredPage) -> PageBuilder:
        for table in page.tables:
            builder = (
                builder.with_table()  # type: ignore
                .with_column_count(table.column_count)
                .with_row_count(table.row_count)
                .with_polygon(page.convert_bounding_region_to_polygon(table.bounding_regions[FIRST_ELEMENT]))
            )
            builder = self._add_cells(table=table, builder=builder, page=page)

        return builder

    def _add_cells(self, table: DocumentTable, builder: TableBuilder, page: StructuredPage) -> CellBuilder:
        for cell in table.cells:
            builder = (
                builder.with_cell()  # type: ignore
                .with_content(cell.content)
                .with_column_index(cell.column_index)
                .with_column_span(cell.column_span)
                .with_row_index(cell.row_index)
                .with_row_span(cell.row_span)
                .with_polygon(page.convert_bounding_region_to_polygon(cell.bounding_regions[FIRST_ELEMENT]))
                .with_kind(cell.kind)
            )

        return builder

    def _add_key_value_pairs(self, builder: PageBuilder, page: StructuredPage) -> PageBuilder:
        for key_value_pair in page.key_value_pairs:
            # fmt: off
            builder = (  # type: ignore
                builder.with_key_value_pair()
                .with_confidence(key_value_pair.confidence)
            )
            # fmt: on
            builder = self._add_key_value_pair_element(
                builder=builder.with_key(),
                element=key_value_pair.key,
                page=page,
            )

            if key_value_pair.value:
                builder = self._add_key_value_pair_element(
                    builder=builder.with_value(),
                    element=ValueResponse.with_value(key_value_pair.value),
                    page=page,
                )

        return builder

    def _add_key_value_pair_element(
        self,
        builder: KeyValuePairElementBuilder,
        element: DocumentKeyValueElement,
        page: StructuredPage,
    ) -> KeyValuePairElementBuilder:
        # fmt: off
        return (
            builder
            .with_content(element.content)
            .with_polygon(page.convert_bounding_region_to_polygon(element.bounding_regions[FIRST_ELEMENT]))
        )
        # fmt: on

    def _add_paragraphs(self, builder: PageBuilder, page: StructuredPage) -> LineBuilder:
        for paragraph in page.paragraphs:
            builder = (  # type: ignore
                builder.with_paragraph()
                .with_content(paragraph.content)
                .with_role(paragraph.role)
                .with_polygon(
                    page.convert_bounding_region_to_polygon(paragraph.bounding_regions[FIRST_ELEMENT]),
                )
            )

            builder = self._add_lines(builder=builder, paragraph=paragraph, page=page)

        return builder

    def _add_lines(self, builder: ParagraphBuilder, paragraph: DocumentParagraph, page: StructuredPage) -> LineBuilder:
        for line in page.lines_of(paragraph):
            builder = (  # type: ignore
                builder.with_line()
                .with_content(line.content)
                .with_polygon(page.convert_abs_coordinates_to_relative(line.polygon))
            )
            builder = self._add_words(line=line, builder=builder, page=page)
            builder = self._add_selection_marks(line=line, builder=builder, page=page)
            builder = self._add_barcodes(line=line, builder=builder, page=page)
            builder = self._add_formulas(line=line, builder=builder, page=page)

        return builder

    def _add_words(self, line: DocumentLine, builder: LineBuilder, page: StructuredPage) -> LineBuilder:
        for word in page.words_of(line):
            builder = (
                builder.with_word()
                .with_content(word.content)
                .with_polygon(page.convert_abs_coordinates_to_relative(word.polygon))
                .with_confidence(word.confidence)
            )
            builder = self._add_style(word, builder)

        return builder

    def _add_style(self, word: DocumentWord, builder: WordBuilder) -> WordBuilder:
        if style := self._response.style_of(word):
            return builder.with_style(
                background_color=style.background_color,
                color=style.color,
                bold=style.font_weight == "bold",
                italic=style.font_style == "italic",
                handwritten=style.is_handwritten,
                font_type=style.similar_font_family,
            )

        return builder.with_style()

    def _add_selection_marks(self, line: DocumentLine, builder: LineBuilder, page: StructuredPage) -> LineBuilder:
        for selection_mark in page.selection_marks_of(line):
            builder = (
                builder.with_selection_mark()
                .with_state(selection_mark.state)
                .with_confidence(selection_mark.confidence)
                .with_polygon(page.convert_abs_coordinates_to_relative(selection_mark.polygon))
            )

        return builder

    def _add_barcodes(self, line: DocumentLine, builder: LineBuilder, page: StructuredPage) -> LineBuilder:
        for barcode in page.barcodes_of(line):
            builder = (
                builder.with_barcode()
                .with_value(barcode.value)
                .with_kind(barcode.kind)
                .with_confidence(barcode.confidence)
                .with_polygon(page.convert_abs_coordinates_to_relative(barcode.polygon))
            )

        return builder

    def _add_formulas(self, line: DocumentLine, builder: LineBuilder, page: StructuredPage) -> LineBuilder:
        for formula in page.formulas_of(line):
            builder = (
                builder.with_formula()
                .with_value(formula.value)
                .with_kind(formula.kind)
                .with_confidence(formula.confidence)
                .with_polygon(page.convert_abs_coordinates_to_relative(formula.polygon))
            )

        return builder
