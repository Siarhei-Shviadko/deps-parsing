import pytest
from deps_tabular_layout.models import ParsingType, TabularLayoutFactory

from deps_parsing.infrastructure.exceptions import ParsingCsvError


def test_parser__ok(csv_parser_with_fakes, test_csv_data, fake_document_proxy, document_id, tenant_id):
    test_file, cell_count, cols, rows = test_csv_data
    tl = TabularLayoutFactory.make_empty_layout(
        document_id=document_id,
        tenant_id=tenant_id,
        parsing_type=ParsingType.CSV,
    )

    fake_document_proxy.set_mocked_file(test_file)

    csv_parser_with_fakes.parse(tl)

    assert len(tl.sheets) == 1
    assert len(tl.sheets[0].tables) == 1
    assert len(csv_parser_with_fakes._cell_repository._db) == cell_count
    assert tl.sheets[0].tables[0].column_count == cols
    assert tl.sheets[0].tables[0].row_count == rows
    assert (tl.sheets[0].tables[0].placement[0].x, tl.sheets[0].tables[0].placement[0].y) == (0, 0)
    assert (tl.sheets[0].tables[0].placement[1].x, tl.sheets[0].tables[0].placement[1].y) == (cols - 1, rows - 1)


def test_parser_empty_csv__error_raised(
    csv_parser_with_fakes,
    test_empty_csv_data,
    fake_document_proxy,
    document_id,
    tenant_id,
):
    tl = TabularLayoutFactory.make_empty_layout(
        document_id=document_id,
        tenant_id=tenant_id,
        parsing_type=ParsingType.CSV,
    )
    fake_document_proxy.set_mocked_file(test_empty_csv_data)

    with pytest.raises(ParsingCsvError):
        csv_parser_with_fakes.parse(tl)


def test_parser__batch_saving__correct(
    csv_parser_with_mocked_repo,
    test_base_csv_file,
    fake_document_proxy,
    document_id,
    tenant_id,
):
    csv_parser_with_mocked_repo._CELL_BATCH_SIZE = 3
    tl = TabularLayoutFactory.make_empty_layout(
        document_id=document_id,
        tenant_id=tenant_id,
        parsing_type=ParsingType.CSV,
    )
    fake_document_proxy.set_mocked_file(test_base_csv_file)

    csv_parser_with_mocked_repo.parse(tl)

    assert (
        csv_parser_with_mocked_repo._cell_repository.save_batch.call_count
        == 12 / csv_parser_with_mocked_repo._CELL_BATCH_SIZE
    )
