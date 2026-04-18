import pytest
from deps_document_layout.model import DocumentLayout, ParsingType
from deps_document_layout.serializers.document_layout import SerializedDocumentLayout

from deps_parsing.domain.services.split_tables_detection.tables_group import TablesGroup


@pytest.fixture
def document_layout_loader():
    class _DlLoader:
        def load(self, path: str) -> DocumentLayout:
            with open(path, "r") as file:
                return SerializedDocumentLayout.parse_raw(file.read()).to_model("tenant-id")

    return _DlLoader()


@pytest.fixture
def dl__headers__indexing__column_count(document_layout_loader):
    return document_layout_loader.load("tests/data/document_layouts/dl_headers,indexing,column-count.json")


@pytest.fixture
def dl__headers__indexing__crap_tables(document_layout_loader):
    return document_layout_loader.load("tests/data/document_layouts/dl_headers,indexing,many-tables.json")


@pytest.fixture
def dl__columns_alignment_only(document_layout_loader):
    return document_layout_loader.load("tests/data/document_layouts/dl_columns_alignment_only.json")


@pytest.fixture
def dl__has_text_between__but_all_markers(document_layout_loader):
    return document_layout_loader.load("tests/data/document_layouts/dl_all_but_text_between.json")


@pytest.fixture
def dl__random_tables(document_layout_loader):
    return document_layout_loader.load("tests/data/document_layouts/dl_random_tables.json")


@pytest.fixture
def dl__complex_case(document_layout_loader):
    return document_layout_loader.load("tests/data/document_layouts/dl__complex_case.json")


@pytest.fixture
def tables_group():
    return TablesGroup(parsing_type=ParsingType.AZURE_FORM_RECOGNIZER)
