from deps_parsing.infrastructure.repositories.document_layout.mappers import (
    DocumentLayoutMapper,
)
from tests.data import raw_document_layout_from_db
from tests.data.document_layout import document_layout


def test_to_dict__ok():
    layout_data = DocumentLayoutMapper.to_dict(document_layout)

    layout_dict = layout_data["document_layout"]
    assert layout_dict["id"] == document_layout.id()
    assert layout_dict["merged_tables"] == document_layout.merged_tables
    assert layout_dict["parsing_features"] == {
        pt.value: [pf.value for pf in pfs] for pt, pfs in document_layout.parsing_features.items()
    }
    assert layout_dict["tenant_id"] == document_layout.tenant_id()

    pages_dict = layout_data["pages"]
    assert pages_dict["pages"]
    assert pages_dict["images"]
    assert pages_dict["paragraphs"]
    assert pages_dict["tables"]
    assert pages_dict["key_value_pairs"]


def test_from_dict__ok():
    layout = DocumentLayoutMapper.from_dict(raw_document_layout_from_db)

    assert layout.id() == raw_document_layout_from_db["id"]
    assert layout.tenant_id() == raw_document_layout_from_db["tenant_id"]
    assert layout.parsing_features
    assert layout.pages
    assert layout.merged_tables
