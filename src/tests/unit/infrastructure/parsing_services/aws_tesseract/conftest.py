import json
from pathlib import Path
from unittest.mock import Mock

import pytest
from deps_document_layout.model import Point
from textractor.parsers import response_parser

from deps_parsing.infrastructure.dl_parsing import (
    AWSTextractDocumentParsingService,
    AWSTextractPageParsingService,
    ParsedImage,
)
from deps_parsing.infrastructure.dl_parsing.aws_textract.parser import AwsTextractParser
from tests.fakes import FakeAWSTextractProxy


def parse_file(filename) -> dict:
    with Path(filename).open() as file:
        return json.loads(file.read())


@pytest.fixture
def page1_dict():
    return parse_file("tests/data/aws_textract/page1_ocr_result.json")


@pytest.fixture
def page2_dict():
    return parse_file("tests/data/aws_textract/page2_ocr_result.json")


@pytest.fixture
def page_1_2_dict():
    return parse_file("tests/data/aws_textract/page_1_2_ocr_result.json")


@pytest.fixture
def page_with_image_dict():
    return parse_file("tests/data/aws_textract/page_with_image.json")


@pytest.fixture
def page_with_checkbox_inside_table_cell_dict():
    return parse_file("tests/data/aws_textract/page_with_checkbox_in_table.json")


@pytest.fixture
def page1_aws_document(page1_dict):
    return response_parser.parse(page1_dict)


@pytest.fixture
def page2_aws_document(page2_dict):
    return response_parser.parse(page2_dict)


@pytest.fixture
def page_with_image_aws_document(page_with_image_dict):
    return response_parser.parse(page_with_image_dict)


@pytest.fixture
def page_with_checkbox_inside_table_cell_aws_document(page_with_checkbox_inside_table_cell_dict):
    return response_parser.parse(page_with_checkbox_inside_table_cell_dict)


@pytest.fixture
def fake_aws_proxy(containers):
    with containers.external_services.aws_textract.override(FakeAWSTextractProxy()):
        yield containers.external_services.aws_textract()


@pytest.fixture
def fake_aws_proxy_page1_response(fake_aws_proxy, page1_dict):
    fake_aws_proxy.response = page1_dict
    return fake_aws_proxy


@pytest.fixture
def fake_aws_proxy_page2_response(fake_aws_proxy, page2_dict):
    fake_aws_proxy.response = page2_dict
    return fake_aws_proxy


@pytest.fixture
def fake_aws_proxy_page_1_2_response(fake_aws_proxy, page_1_2_dict):
    fake_aws_proxy.response = page_1_2_dict
    return fake_aws_proxy


@pytest.fixture
def aws_textract_engine(fake_aws_proxy, containers):
    return containers.engines.aws_textract()


@pytest.fixture
def aws_textract_page1_engine(fake_aws_proxy_page1_response, containers):
    return containers.engines.aws_textract()


@pytest.fixture
def aws_textract_page_1_2_engine(fake_aws_proxy_page_1_2_response, containers):
    return containers.engines.aws_textract()


@pytest.fixture
def fake_blob():
    return b"Fake blob"


@pytest.fixture
def page1_textract_parser(document_layout, page1_aws_document, unified_data_image_page1):
    return AwsTextractParser(
        aws_page=page1_aws_document.page(0),
        image=unified_data_image_page1,
        parsed_page_images=[],
    )


@pytest.fixture
def page2_textract_parser(document_layout, page2_aws_document, unified_data_image_page1):
    return AwsTextractParser(aws_page=page2_aws_document.page(0), image=unified_data_image_page1, parsed_page_images=[])


@pytest.fixture
def parsed_image() -> ParsedImage:
    return ParsedImage(
        title="some-title",
        description="some-description",
        filepath="/some/path/to/image.png",
        page_coordinates=(Point(0.1, 0.1), Point(0.2, 0.2)),
    )


@pytest.fixture
def page_with_image_parser(document_layout, page_with_image_aws_document, unified_data_image_page1, parsed_image):
    return AwsTextractParser(
        aws_page=page_with_image_aws_document.page(0),
        image=unified_data_image_page1,
        parsed_page_images=[parsed_image],
    )


@pytest.fixture
def page_with_checkbox_inside_table_cell_parser(
    document_layout, page_with_checkbox_inside_table_cell_aws_document, unified_data_image_page1
):
    return AwsTextractParser(
        aws_page=page_with_checkbox_inside_table_cell_aws_document.page(0),
        image=unified_data_image_page1,
        parsed_page_images=[],
    )


@pytest.fixture
def totally_mocked_aws_parsing_service(
    unifier_mock,
    storage_mock,
    aws_textract_page1_engine,
    unified_data_image_page1,
    ocr_image_processing_service,
):
    unifier_mock.get_original_images.return_value = [unified_data_image_page1]
    storage_mock.download.return_value = b"File content"
    return AWSTextractPageParsingService(
        unifier=unifier_mock,
        storage=storage_mock,
        engine=aws_textract_page1_engine,
        image_processing_service=ocr_image_processing_service,
    )


@pytest.fixture
def totally_mocked_aws_document_parsing_service(
    mocker,
    unifier_mock,
    storage_mock,
    document_mock,
    file_mock,
    aws_textract_page_1_2_engine,
    unified_data_image_page1,
    unified_data_image_page2,
    ocr_image_processing_service,
):
    unifier_mock.get_original_images.return_value = [unified_data_image_page1, unified_data_image_page2]
    storage_mock.download.return_value = b"File content"
    document_mock.get_brief_document_info.return_value = {"id": "123", "files": "test_blob.pdf", "title": "test.pdf"}

    aws_storage_mock = Mock(name="aws_storage_mock")
    mocker.patch(
        "deps_parsing.infrastructure.dl_parsing.aws_textract.document_service.make_aws_object_storage",
        return_value=aws_storage_mock,
    )

    return AWSTextractDocumentParsingService(
        unifier=unifier_mock,
        storage=storage_mock,
        engine=aws_textract_page_1_2_engine,
        image_processing_service=ocr_image_processing_service,
        document=document_mock,
        file=file_mock,
        s3_bucket_name="test",
        parallelism_factor=5,
    )
