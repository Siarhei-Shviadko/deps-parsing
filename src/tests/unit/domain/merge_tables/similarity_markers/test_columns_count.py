import pytest

from deps_parsing.domain.services.split_tables_detection.similarity_markers import (
    ColumnsCountMarker,
)


@pytest.mark.parametrize(
    "layout_fixture_name, expected",
    [
        ("dl__headers__indexing__column_count", True),
        ("dl__headers__indexing__crap_tables", True),
        ("dl__columns_alignment_only", True),
        ("dl__random_tables", False),
    ],
)
def test_columns_count(layout_fixture_name, expected, request):
    layout = request.getfixturevalue(layout_fixture_name)

    first_page = layout.pages[0]
    second_page = layout.pages[1]

    assert ColumnsCountMarker().is_present(first_page, second_page) == expected
