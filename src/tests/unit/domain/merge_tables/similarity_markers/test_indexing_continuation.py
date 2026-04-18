import pytest

from deps_parsing.domain.services.split_tables_detection.similarity_markers import (
    IndexingContinuationMarker,
)


@pytest.mark.parametrize(
    "previous_label, next_label, expected",
    [
        pytest.param("c", "d", True),
        pytest.param("c.", "d.", True),
        pytest.param("c)", "d)", True),
        pytest.param("c.", "d", True),
        pytest.param("edqwevv c", "d", False),
        pytest.param("5", "6", True),
        pytest.param("5.", "6", True),
        pytest.param("some text 5", "6", False),
        pytest.param("some text 5", "hahaha 6 text 6", False),
    ],
)
def test__is_valid_label_format(previous_label: str, next_label: str, expected: bool) -> None:
    assert IndexingContinuationMarker()._is_valid_label_format(previous_label, next_label) == expected


@pytest.mark.parametrize(
    "previous_label, next_label, expected",
    [
        pytest.param("3", "4", True),
        pytest.param("5", "8", False),
        pytest.param("c.", "d.", False),
    ],
)
def test__is_sequential_number(previous_label: str, next_label: str, expected: bool) -> None:
    assert IndexingContinuationMarker()._is_numeric_continuation(previous_label, next_label) == expected


@pytest.mark.parametrize(
    "previous_label, next_label, expected",
    [
        pytest.param("3", "4", False),
        pytest.param("c", "f", False),
        pytest.param("c.", "d.", True),
    ],
)
def test__is_alphabetical_continuation(previous_label: str, next_label: str, expected: bool) -> None:
    assert IndexingContinuationMarker()._is_alphabetical_continuation(previous_label, next_label) == expected


@pytest.mark.parametrize(
    "previous_label, next_label, expected",
    [
        pytest.param("c", "d", True),
        pytest.param("c.", "d.", True),
        pytest.param("c)", "d)", True),
        pytest.param("c.", "d", True),
        pytest.param("edqwevv c", "d", False),
        pytest.param("5", "6", True),
        pytest.param("5.", "6.", True),
        pytest.param("3.", "1.", False),
        pytest.param("5.", "8.", False),
        pytest.param("some text 5", "6", False),
        pytest.param("some text 5", "hahaha 6 text 6", False),
    ],
)
def test__check(previous_label: str, next_label: str, expected: bool) -> None:
    assert IndexingContinuationMarker()._check_if_continuous_indexing(previous_label, next_label) == expected


@pytest.mark.parametrize(
    "label, expected",
    [
        pytest.param("1", 1),
        pytest.param("1.", 1),
    ],
)
def test__extract_label_number(label: str, expected: int) -> None:
    assert IndexingContinuationMarker()._extract_label_number(label) == expected


@pytest.mark.parametrize(
    "label, expected",
    [
        pytest.param("a", "a"),
    ],
)
def test__extract_label_char(label: str, expected: str) -> None:
    assert IndexingContinuationMarker()._extract_label_char(label) == expected
