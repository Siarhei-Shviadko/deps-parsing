from deps_document_layout.model import DocumentLayout, Page, Point

from deps_parsing.domain.model import CheckmarkValue
from deps_parsing.infrastructure import UnifiedDataImage
from deps_parsing.infrastructure.dl_parsing.google.parser import (
    DocAIDocument,
    DocumentAIResponseParser,
)


def test_response_parsing(
    parsed_file__all_types: DocAIDocument,
    document_layout: DocumentLayout,
    unified_data_image_page1: UnifiedDataImage,
):
    parsed_page = parsed_file__all_types.pages[0]
    parser = DocumentAIResponseParser(parsed_file__all_types, parsed_page, unified_data_image_page1)

    parser.add_page_to(document_layout)

    assert len(document_layout.pages) == 1

    page = document_layout.pages[0]

    assert page.dimension.width == 1681
    assert page.dimension.height == 2378
    assert page.dimension.unit == "pixels"

    assert page.page_number == 1
    assert page.id.value == unified_data_image_page1.id
    assert page.file_path == unified_data_image_page1.blob_name

    _assert_paragraphs_correct(page)
    _assert_table_correct(page)
    _assert_key_value_pairs_correct(page)


def _assert_table_correct(page: Page) -> None:
    assert len(page.tables) == 1

    table = page.tables[0]
    assert len(table.cells) == 40
    assert round(table.confidence, 5) == 0.99902
    assert table.column_count == 8
    assert table.row_count == 5

    expected_points = (Point(x=0.12, y=0.43), Point(x=0.95, y=0.43), Point(x=0.95, y=0.59), Point(x=0.12, y=0.59))
    assert tuple([Point(round(p.x, 2), round(p.y, 2)) for p in table.polygon]) == expected_points

    first_cell = table.cells[0]
    assert first_cell.column_index == 0
    assert first_cell.row_index == 0
    assert first_cell.paragraph_id

    found_paragraph = next(filter(lambda p: p.id == first_cell.paragraph_id, page.paragraphs), None)
    assert found_paragraph is not None

    assert found_paragraph.content == "1.1. Accept "
    assert round(found_paragraph.confidence, 7) == 0.9991045

    expected_points = (Point(x=0.12, y=0.43), Point(x=0.22, y=0.43), Point(x=0.22, y=0.44), Point(x=0.12, y=0.44))
    assert tuple([Point(round(p.x, 2), round(p.y, 2)) for p in found_paragraph.polygon]) == expected_points


def _assert_key_value_pairs_correct(page: Page) -> None:
    assert len(page.key_value_pairs) == 2

    kvp1 = page.key_value_pairs[0]
    assert kvp1.value.content == "and\n"
    assert kvp1.key.content == "(full name of enterprise, institution or organization)\n"
    assert kvp1.confidence == 0.9432543516159058
    expected_points = (Point(x=0.30, y=0.26), Point(x=0.69, y=0.26), Point(x=0.69, y=0.28), Point(x=0.30, y=0.28))
    assert tuple([Point(round(p.x, 2), round(p.y, 2)) for p in kvp1.key.polygon]) == expected_points

    kvp2 = page.key_value_pairs[1]
    assert kvp2.key.content == "(occupation, full name)\n"
    assert kvp2.value.content == CheckmarkValue.UNCHECKED
    assert kvp2.confidence == 0.9261502027511597
    expected_points = (Point(x=0.12, y=0.28), Point(x=0.21, y=0.28), Point(x=0.21, y=0.31), Point(x=0.12, y=0.31))
    assert tuple([Point(round(p.x, 2), round(p.y, 2)) for p in kvp2.value.polygon]) == expected_points


def _assert_paragraphs_correct(page: Page) -> None:
    assert len(page.paragraphs) == 54

    first_paragraph = page.paragraphs[0]
    assert first_paragraph.confidence == 0.9928852319717407
    expected_points = (Point(x=0.13, y=0.08), Point(x=0.86, y=0.08), Point(x=0.86, y=0.11), Point(x=0.13, y=0.11))
    assert tuple([Point(round(p.x, 2), round(p.y, 2)) for p in first_paragraph.polygon]) == expected_points
    assert (
        first_paragraph.content
        == "Agreement No\non the organization and conduct of student internship at enterprises, institutions and organizations\n"
    )

    first_line = first_paragraph.lines[0]
    assert first_line.content == "Agreement No\n"
    assert first_line.confidence == 0.962298572063446
    expected_points = (Point(x=0.37, y=0.08), Point(x=0.47, y=0.08), Point(x=0.47, y=0.11), Point(x=0.37, y=0.11))
    assert tuple([Point(round(p.x, 2), round(p.y, 2)) for p in first_line.polygon]) == expected_points

    first_word = first_line.words[0]
    assert first_word.content == "Agreement "
    assert round(first_word.confidence, 7) == 0.9932686
    expected_points = (Point(x=0.37, y=0.08), Point(x=0.45, y=0.08), Point(x=0.45, y=0.11), Point(x=0.37, y=0.11))
    assert tuple([Point(round(p.x, 2), round(p.y, 2)) for p in first_word.polygon]) == expected_points
