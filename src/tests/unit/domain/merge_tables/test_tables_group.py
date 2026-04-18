from deps_document_layout.model import ParsingType, RawTableReference

from deps_parsing.domain.services.split_tables_detection.tables_group import TableRef


def test_tables_group_initialization(tables_group):
    assert tables_group.parsing_type == ParsingType.AZURE_FORM_RECOGNIZER
    assert not tables_group.has_tables()


def test_tables_group_add_table(tables_group, table):
    tables_group.add(for_page=1, table=table)

    assert tables_group.has_tables()
    assert TableRef(page_number=1, table_id=table.id()) in tables_group.tables


def test_tables_group_to_raw(tables_group, table):
    tables_group.add(for_page=1, table=table)
    raw = tables_group.to_raw()

    assert raw["parsing_type"] == ParsingType.AZURE_FORM_RECOGNIZER
    assert raw["tables"] == [RawTableReference(page_number=1, table_id=table.id())]


def test_tables_group_tables_references(tables_group, table):
    tables_group.add(for_page=1, table=table)
    references = tables_group.tables_references()

    assert references == [RawTableReference(page_number=1, table_id=table.id())]
