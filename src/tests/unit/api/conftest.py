import pytest


@pytest.fixture(autouse=True)
def semantic_layout_service_autouse(semantic_layout_service_mock):
    semantic_layout_service_mock.layout_info_for.return_value = None
    yield semantic_layout_service_mock
