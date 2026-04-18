from deps_document_layout.model import DocumentLayout

from deps_parsing.domain.dtos import DocumentLayoutInfo

__all__ = ["compare_2_document_layout_info", "full_compare_2_document_layouts"]


def compare_2_document_layout_info(layout_1: DocumentLayout, layout_info: DocumentLayoutInfo):
    assert layout_1.id() == layout_info.id
    assert layout_1.parsing_features == layout_info.parsing_features
    assert layout_1.merged_tables == layout_info.merged_tables

    pages_parsing_types = {page.parsing_type for page in layout_1.pages}
    counted_pages_per_type__original_layout = {
        parsing_type: sum(1 for page in layout_1.pages if page.parsing_type == parsing_type)
        for parsing_type in pages_parsing_types
    }
    counted_pages_per_type__layout_info = {
        parsing_type: info.pages_count for parsing_type, info in layout_info.pages_info.items()
    }

    assert counted_pages_per_type__original_layout == counted_pages_per_type__layout_info


def full_compare_2_document_layouts(layout_1: DocumentLayout, layout_2: DocumentLayout):
    assert layout_1 == layout_2
    assert layout_1.parsing_features == layout_2.parsing_features
    assert layout_1.merged_tables == layout_2.merged_tables

    for page_from_1, page_from_2 in zip(
        sorted(layout_1.pages, key=lambda page: page.page_number),
        sorted(layout_2.pages, key=lambda page: page.page_number),
    ):
        assert page_from_1 == page_from_2
        assert page_from_1.page_number == page_from_2.page_number
        assert page_from_1.parsing_type == page_from_2.parsing_type
        assert page_from_1.dimension == page_from_2.dimension
        assert page_from_1.languages == page_from_2.languages
        assert page_from_1.file_path == page_from_2.file_path
        assert page_from_1.transformations == page_from_2.transformations
        assert page_from_1.images == page_from_2.images
        assert page_from_1.key_value_pairs == page_from_2.key_value_pairs
        assert page_from_1.tables == page_from_2.tables
        assert page_from_1.paragraphs == page_from_2.paragraphs
        assert page_from_1.groups == page_from_2.groups
