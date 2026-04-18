from uuid import uuid4

from deps_document_layout.model import Page

from deps_parsing.infrastructure.repositories.document_layout.mappers import PageMapper
from tests.data import page_from_db


def test_to_dict__ok(page_factory):
    orig_page: Page = page_factory()
    layout_id = uuid4().hex

    page_dict = PageMapper.to_dict(document_layout_id=layout_id, pages=[orig_page])

    [page_data] = page_dict["pages"]
    orig_dimension = orig_page.dimension
    assert page_data["document_layout_id"] == layout_id
    assert page_data["file_path"] == orig_page.file_path
    assert page_data["groups"] == list(orig_page.groups)
    assert page_data["id"] == orig_page.id()
    assert page_data["page_number"] == orig_page.page_number
    assert page_data["transformations"]
    assert page_data["dimension"] == {
        "width": orig_dimension.width,
        "height": orig_dimension.height,
        "unit": orig_dimension.unit,
    }
    assert page_data["languages"] == [
        {"language_code": l.language_code, "confidence": l.confidence} for l in orig_page.languages
    ]


def test_from_dict__ok():
    restored_page = PageMapper.from_dict(page_from_db)

    dimension = restored_page.dimension
    languages = restored_page.languages
    assert page_from_db["dimension"] == {"height": dimension.height, "width": dimension.width, "unit": dimension.unit}
    assert restored_page.file_path == page_from_db["file_path"]
    assert restored_page.id() == page_from_db["id"]
    assert page_from_db["languages"] == [
        {"language_code": l.language_code, "confidence": l.confidence} for l in languages
    ]
    assert restored_page.page_number == page_from_db["page_number"]
    assert restored_page.parsing_type == page_from_db["parsing_type"]
    assert restored_page.images
    assert restored_page.key_value_pairs
    assert restored_page.paragraphs
    assert restored_page.tables
    assert restored_page.transformations
    assert restored_page.groups
