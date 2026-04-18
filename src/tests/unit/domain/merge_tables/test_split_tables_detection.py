import pytest
from deps_document_layout.model import RawMergedTable

from deps_parsing.domain.services import SplitTablesDetectionService


@pytest.mark.parametrize(
    "layout_fixture_name, expected",
    [
        (
            "dl__has_text_between__but_all_markers",
            [
                {
                    "parsing_type": "AZURE_FORM_RECOGNIZER",
                    "tables": [
                        {"page_number": 1, "table_id": "aa17ee70344c4a06a58d28b4dd656a49"},
                        {"page_number": 2, "table_id": "a95c3f49a9ca43bdb6730f160c9b9617"},
                    ],
                },
            ],
        ),
        (
            "dl__headers__indexing__crap_tables",
            [
                {
                    "parsing_type": "AZURE_FORM_RECOGNIZER",
                    "tables": [
                        {"page_number": 1, "table_id": "e1edaa01530042c1b944c43aebcf5af6"},
                        {"page_number": 2, "table_id": "e32476dfa7fc40ad956fe6bba75fd422"},
                    ],
                },
            ],
        ),
        (
            "dl__random_tables",
            [],
        ),
        (
            "dl__complex_case",
            [
                {
                    "parsing_type": "AZURE_FORM_RECOGNIZER",
                    "tables": [
                        {"page_number": 1, "table_id": "83cd1b6856f74dd69e8c219c2ccc0dbe"},
                        {"page_number": 2, "table_id": "2d901363fd3b4bb0a1a4acd3eb6bc5d0"},
                    ],
                },
                {
                    "parsing_type": "AZURE_FORM_RECOGNIZER",
                    "tables": [
                        {"page_number": 4, "table_id": "1278238cceff49d1b2cd07d0cb031f1e"},
                        {"page_number": 5, "table_id": "c76b6845f28f4373a945c1d760036707"},
                    ],
                },
            ],
        ),
    ],
)
def test_split_tables_detection(
    layout_fixture_name: str,
    expected: set[RawMergedTable],
    split_tables_detection_service: SplitTablesDetectionService,
    request,
):
    layout = request.getfixturevalue(layout_fixture_name)
    default_parsing_type = layout.pages[0].parsing_type

    result = split_tables_detection_service.detect_split_tables(
        layout,
        for_parsing_type=default_parsing_type,
    )

    for result_table, expected_table in zip(result, expected):
        assert result_table.parsing_type == expected_table["parsing_type"]

        for result_table_ref in result_table.tables_references():
            assert result_table_ref in expected_table["tables"]
