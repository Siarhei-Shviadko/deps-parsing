import json

import pytest
from azure.ai.formrecognizer import AnalyzeResult

from deps_parsing.infrastructure.dl_parsing import OCRedPageRawResponse
from deps_parsing.infrastructure.proxies import UnifiedDataImage
from tests.data import unified_image_page1, unified_image_page2


@pytest.fixture
def unified_data_image_page1():
    return UnifiedDataImage.from_dict(unified_image_page1)


@pytest.fixture
def unified_data_image_page2():
    return UnifiedDataImage.from_dict(unified_image_page2)


@pytest.fixture
def azure_response_page1_dict() -> OCRedPageRawResponse:
    with open("tests/data/azure/page1.json", "r") as f:
        return json.loads(f.read())


@pytest.fixture
def azure_response_page2_dict() -> OCRedPageRawResponse:
    with open("tests/data/azure/page2.json", "r") as f:
        return json.loads(f.read())


@pytest.fixture
def azure_response_two_pages_dict() -> OCRedPageRawResponse:
    with open("tests/data/azure/two_pages.json", "r") as f:
        return json.loads(f.read())


@pytest.fixture
def azure_analyze_result_page1(azure_response_page1_dict) -> AnalyzeResult:
    return AnalyzeResult.from_dict(azure_response_page1_dict)


@pytest.fixture
def azure_analyze_result_page2(azure_response_page2_dict) -> AnalyzeResult:
    return AnalyzeResult.from_dict(azure_response_page2_dict)


@pytest.fixture
def azure_analyze_result_two_pages(azure_response_two_pages_dict) -> AnalyzeResult:
    return AnalyzeResult.from_dict(azure_response_two_pages_dict)


@pytest.fixture
def lite_azure_proxy_response(azure_analyze_result_page1):
    class LROPoller:
        @classmethod
        def result(cls):
            return azure_analyze_result_page1

    return LROPoller
