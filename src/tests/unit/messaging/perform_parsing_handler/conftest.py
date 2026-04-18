from copy import deepcopy
from unittest.mock import patch
from uuid import uuid4

import pytest
from deps_document_layout.model import ParsingFeature
from deps_message_flow.commands.consumer import CommandMessage
from deps_object_storage import ObjectStorage
from more_itertools import first

from deps_parsing.application.parsing_type import DLParsingType
from deps_parsing.messaging.commands import PerformParsing
from tests.data import ocr_response_, unified_image_page1
from tests.fakes import FakeCloudObjectStorageProxy, FakeUnifierProxy

CSV_FILE_PATH, EXCEL_FILE_PATH, DOCX_FILE_PATH = f"{uuid4().hex}.csv", f"{uuid4().hex}.xlsx", f"{uuid4().hex}.docx"


@pytest.fixture
def save_docx_content_to_storage(fake_file_storage_proxy: ObjectStorage, docx_file_with_paragraph_and_table) -> None:
    fake_file_storage_proxy.upload(
        path=DOCX_FILE_PATH,
        content=docx_file_with_paragraph_and_table,
        replace_if_exists=True,
    )


@pytest.fixture
def save_excel_content_to_storage(fake_file_storage_proxy: ObjectStorage, excel_file_all_styles) -> None:
    fake_file_storage_proxy.upload(path=EXCEL_FILE_PATH, content=excel_file_all_styles, replace_if_exists=True)


@pytest.fixture
def save_csv_content_to_storage(fake_file_storage_proxy: ObjectStorage, csv_base_file) -> None:
    fake_file_storage_proxy.upload(path=CSV_FILE_PATH, content=csv_base_file, replace_if_exists=True)


@pytest.fixture
def parsing_features() -> set[ParsingFeature]:
    return {ParsingFeature.TABLES, ParsingFeature.TEXT}


@pytest.fixture
def tesseract_engine_mock(tesseract_engine_mock, parsing_features):
    tesseract_engine_mock.recognize_blob.return_value = {"ocr_data": ocr_response_}
    tesseract_engine_mock.fetch_received_features.return_value = parsing_features


@pytest.fixture
def save_unified_data(entity_id: str, fake_unifier_proxy: FakeUnifierProxy, file_path):
    copied_image = deepcopy(unified_image_page1)
    copied_image["originalImageId"] = None
    copied_image["blobName"] = file_path

    fake_unifier_proxy.save(entity_id=entity_id, udata={"elements": [copied_image]})


@pytest.fixture
def perform_parsing_command_message_without_features(mocker, tenant_id, entity_id, file_path):
    command_message = mocker.Mock(CommandMessage)
    command_message.command = PerformParsing(
        tenant_id=tenant_id,
        document_id=entity_id,
        files=[file_path],
        engine=None,
        features=set(),
        document_type_id=None,
        language=None,
    )

    return command_message


@pytest.fixture
def fake_aws_object_storage():
    with patch(
        "deps_parsing.infrastructure.dl_parsing.v2.aws_textract.document_service.make_aws_object_storage"
    ) as mock:
        mock.return_value = FakeCloudObjectStorageProxy()

        yield mock


@pytest.fixture
def fake_gcp_object_storage():
    with patch("deps_parsing.infrastructure.dl_parsing.v2.google.document_service.make_gcp_object_storage") as mock:
        mock.return_value = FakeCloudObjectStorageProxy()

        yield mock


@pytest.fixture
def prepare_dl_services(request):
    request.getfixturevalue("fake_gcp_document_ai_proxy")
    request.getfixturevalue("fake_gcp_object_storage")
    request.getfixturevalue("fake_aws_textract_proxy")
    request.getfixturevalue("fake_aws_object_storage")
    request.getfixturevalue("fake_azure_proxy")
    request.getfixturevalue("tesseract_engine_mock")
    request.getfixturevalue("save_content_to_storage")
    request.getfixturevalue("save_unified_data")


@pytest.fixture
def prepare_tl_services(tl_perform_parsing_command_message, request):
    file_path: str = first(tl_perform_parsing_command_message.command.files)

    request.getfixturevalue("fake_cell_command_repository")
    request.getfixturevalue("fake_tl_command_repository")
    request.getfixturevalue("fake_gcp_object_storage")
    request.getfixturevalue("fake_aws_object_storage")

    if file_path.endswith(".xlsx"):
        request.getfixturevalue("save_excel_content_to_storage")
    elif file_path.endswith(".csv"):
        request.getfixturevalue("save_csv_content_to_storage")


@pytest.fixture
def perform_parsing_command(tenant_id, entity_id, file_path, parsing_features) -> PerformParsing:
    return PerformParsing(
        tenant_id=tenant_id,
        document_id=entity_id,
        files=[file_path],
        engine=None,
        features=parsing_features,
        document_type_id=None,
        language=None,
    )


@pytest.fixture(
    params=[
        DLParsingType.GCP_VISION,
        DLParsingType.AWS_TEXTRACT,
        DLParsingType.AZURE_FORM_RECOGNIZER,
        DLParsingType.TESSERACT,
    ]
)
def dl_perform_parsing_command_message(perform_parsing_command, mocker, request):
    perform_parsing_command.engine = request.param

    command_message = mocker.Mock(CommandMessage)
    command_message.command = perform_parsing_command

    return command_message


@pytest.fixture(
    params=[
        CSV_FILE_PATH,
        EXCEL_FILE_PATH,
    ]
)
def tl_perform_parsing_command_message(perform_parsing_command, mocker, request):
    perform_parsing_command.files = [request.param]

    command_message = mocker.Mock(CommandMessage)
    command_message.command = perform_parsing_command

    return command_message


@pytest.fixture
def docx_perform_parsing_command_message(perform_parsing_command, mocker):
    perform_parsing_command.files = [DOCX_FILE_PATH]

    command_message = mocker.Mock(CommandMessage)
    command_message.command = perform_parsing_command

    return command_message
