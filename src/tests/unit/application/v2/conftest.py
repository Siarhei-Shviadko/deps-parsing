import pytest

from deps_parsing.application.v2 import SemanticLayoutApplicationV2
from deps_parsing.application.v2.parsing import ParsingService


@pytest.fixture
def semantic_layout_application_v2_mock(containers, mocker):
    mock = mocker.Mock(SemanticLayoutApplicationV2)
    with containers.applications.semantic_layout_application_v2.override(mock):
        yield mock


@pytest.fixture
def document_layout_service_v2_mock(containers, mocker):
    mock = mocker.Mock(containers.applications.document_layout_service_v2.cls)
    with containers.applications.document_layout_service_v2.override(mock):
        yield mock


@pytest.fixture
def tabular_layout_service_v2_mock(containers, mocker):
    mock = mocker.Mock(containers.applications.tabular_layout_service_v2.cls)
    with containers.applications.tabular_layout_service_v2.override(mock):
        yield mock


@pytest.fixture
def parsing_service_v2(
    containers,
    semantic_layout_application_v2_mock,
    document_layout_service_v2_mock,
    tabular_layout_service_v2_mock,
) -> ParsingService:
    return containers.applications.parsing_service_v2()
