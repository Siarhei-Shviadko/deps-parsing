from copy import deepcopy
from unittest.mock import Mock

import pytest
from deps_message_flow.events.subscriber.domain_event_envelope import (
    DomainEventEnvelope,
)
from deps_object_storage import ObjectStorage
from deps_tabular_layout.models import ParsingType as TLParsingType
from deps_tabular_layout.models import TabularLayout, TabularLayoutFactory
from faker.proxy import Faker

from deps_parsing import api
from deps_parsing.application import (
    DocumentLayoutService,
    DocumentTypeService,
    ParsingService,
    SemanticLayoutService,
    TabularLayoutService,
)
from deps_parsing.domain.dtos import SemanticLayoutInfo
from deps_parsing.infrastructure.dl_parsing import (
    AzureOCREngine,
    OCRLayoutImageProcessingService,
)
from deps_parsing.infrastructure.proxies.semantic_layout_info_mapper import (
    SemanticLayoutInfoMapper,
)
from deps_parsing.infrastructure.tl_parsing import ExcelParser
from deps_parsing.messaging.events import FileDeleted
from tests.data.document_layout import document_layout as full_document_layout
from tests.data.semantic_layout_info import semantic_layout_info_payload
from tests.data.tabular_layout import tabular_layout as full_tabular_layout
from tests.fakes import (
    FakeCellCommandRepository,
    FakeDocumentLayoutRepository,
    FakeDocumentProxy,
    FakeObjectStorageProxy,
    FakeTabularLayoutCommandQueryRepository,
)

from ..shared_document_layout_fixtures.update_document_layout_fixtures import *


@pytest.fixture
def postgres_datasource_mock(mocker, containers):
    mock = mocker.Mock(containers.datasources.postgres_datasource())
    containers.datasources.postgres_datasource.override(mock)

    yield mock

    containers.datasources.reset_override()


@pytest.fixture
def fake_file_storage_proxy(containers):
    with containers.external_services.object_storage.override(FakeObjectStorageProxy()) as fsp:
        yield fsp()


@pytest.fixture
def fake_cell_command_repository(containers):
    with containers.repositories.cell_command.override(FakeCellCommandRepository()) as fcc:
        yield fcc()


@pytest.fixture
def cell_command_repository_mock(repositories, mocker):
    mock = mocker.Mock(repositories.cell_command.cls)
    with repositories.cell_command.override(mock):
        yield mock


@pytest.fixture
def fake_document_proxy(containers):
    with containers.external_services.document.override(FakeDocumentProxy()) as fdp:
        yield fdp()


@pytest.fixture
def fake_tl_repository():
    with FakeTabularLayoutCommandQueryRepository() as ftl:
        yield ftl


@pytest.fixture
def fake_tl_command_repository(containers, fake_tl_repository):
    with containers.repositories.tabular_layout_command.override(fake_tl_repository) as ftlc:
        yield ftlc()


@pytest.fixture
def fake_tl_query_repository(containers, fake_tl_repository):
    with containers.repositories.tabular_layout_query.override(fake_tl_repository) as ftlq:
        yield ftlq()


@pytest.fixture(autouse=True)
def raw_document_layout_repository(repositories, fake_file_storage_proxy):
    return repositories.raw_document_layout()


@pytest.fixture(autouse=True)
def document_layout_repository(containers):
    with containers.repositories.document_layout.override(FakeDocumentLayoutRepository()) as dlr:
        yield dlr()


@pytest.fixture(autouse=True)
def gcp_mock(mocker):
    gcp_storage_mock = Mock(name="gcp_storage_mock")
    mocker.patch(
        "deps_parsing.infrastructure.dl_parsing.google.document_service.make_gcp_object_storage",
        return_value=gcp_storage_mock,
    )


@pytest.fixture(autouse=True)
def aws_mock(mocker):
    aws_object_storage = Mock(name="aws_storage_mock")
    mocker.patch(
        "deps_parsing.infrastructure.dl_parsing.aws_textract.document_service.make_aws_object_storage",
        return_value=aws_object_storage,
    )


@pytest.fixture
def raw_document_layout_repository_mock(repositories, mocker):
    mock = mocker.Mock(repositories.raw_document_layout.cls)
    with repositories.raw_document_layout.override(mock):
        yield mock


@pytest.fixture
def document_layout_service(containers) -> DocumentLayoutService:
    return containers.applications.document_layout_service()


@pytest.fixture
def document_type_service(containers) -> DocumentTypeService:
    return containers.applications.document_type_service()


@pytest.fixture
def mocked_excel_parser(mocker) -> ExcelParser:
    return mocker.Mock(ExcelParser)


@pytest.fixture
def tabular_layout_service__with_mocked_excel_parser(
    fake_tl_command_repository,
    fake_tl_query_repository,
    mocked_excel_parser,
    fake_cell_command_repository,
    fake_domain_event_publisher,
) -> TabularLayoutService:
    return TabularLayoutService(
        parsing_service_mapper={
            TLParsingType.EXCEL: mocked_excel_parser,
        },
        tl_command_repository=fake_tl_command_repository,
        tl_query_repository=fake_tl_query_repository,
        cell_command_repository=fake_cell_command_repository,
        domain_event_publisher=fake_domain_event_publisher,
    )


@pytest.fixture
def parsing_service(containers) -> ParsingService:
    return containers.applications.parsing_service()


@pytest.fixture
def document_layout_service_mock(containers, mocker):
    mock = mocker.Mock(containers.applications.document_layout_service.cls)
    with containers.applications.document_layout_service.override(mock):
        yield mock


@pytest.fixture
def semantic_parsing_proxy_mock(external_services, mocker):
    mock = mocker.Mock(external_services.semantic_parsing.cls)
    with external_services.semantic_parsing.override(mock):
        yield mock


@pytest.fixture
def semantic_layout_service(semantic_parsing_proxy_mock, containers) -> SemanticLayoutService:
    return containers.applications.semantic_layout_service()


@pytest.fixture
def semantic_layout_info() -> SemanticLayoutInfo:
    return SemanticLayoutInfoMapper.from_dict(semantic_layout_info_payload, layout_id="document-123")


@pytest.fixture
def semantic_layout_service_mock(containers, mocker):
    mock = mocker.Mock(containers.applications.semantic_layout_service.cls)
    with containers.applications.semantic_layout_service.override(mock):
        yield mock


@pytest.fixture
def tabular_layout_service_mock(containers, mocker):
    mock = mocker.Mock(containers.applications.tabular_layout_service.cls)
    with containers.applications.tabular_layout_service.override(mock):
        yield mock


@pytest.fixture
def document_layout_repository_mock(repositories, mocker):
    mock = mocker.Mock(repositories.document_layout.cls)
    with repositories.document_layout.override(mock):
        yield mock


@pytest.fixture
def document_type_repository_mock(repositories, mocker):
    mock = mocker.Mock(repositories.document_type.cls)
    with repositories.document_type.override(mock):
        yield mock


@pytest.fixture
def parsing_service_mapper(containers):
    return containers.applications.document_layout_service.kwargs["parsing_service_mapper"]


@pytest.fixture
def azure_page_parsing_service_mock(parsing_service_mapper, mocker):
    mock = mocker.Mock(parsing_service_mapper.kwargs["AZURE_FORM_RECOGNIZER"].by_page.cls)
    with parsing_service_mapper.kwargs["AZURE_FORM_RECOGNIZER"].override(mock):
        yield mock


@pytest.fixture
def azure_document_parsing_service_mock(parsing_service_mapper, mocker):
    mock = mocker.Mock(parsing_service_mapper.kwargs["AZURE_FORM_RECOGNIZER"].by_document.cls)
    with parsing_service_mapper.kwargs["AZURE_FORM_RECOGNIZER"].override(mock):
        yield mock


@pytest.fixture
def unifier_mock(external_services, mocker):
    mock = mocker.Mock(external_services.unifier.cls)
    with external_services.unifier.override(mock):
        yield mock


@pytest.fixture
def document_mock(external_services, mocker):
    mock = mocker.Mock(external_services.document.cls)
    with external_services.document.override(mock):
        yield mock


@pytest.fixture(autouse=True)
def file_mock(external_services, mocker):
    mock = mocker.Mock(external_services.file.cls)
    with external_services.file.override(mock):
        yield mock


@pytest.fixture
def azure_proxy_mock(external_services, mocker):
    mock = mocker.Mock(external_services.azure.cls)
    with external_services.azure.override(mock):
        yield mock


@pytest.fixture
def storage_mock(external_services, mocker):
    real_storage = external_services.object_storage()
    mock = mocker.Mock(spec=real_storage)
    with external_services.object_storage.override(mock):
        yield mock


@pytest.fixture
def ai_fusion_mock(external_services, mocker):
    mock = mocker.Mock(external_services.ai_fusion.cls)
    with external_services.ai_fusion.override(mock):
        yield mock


@pytest.fixture
def azure_engine(engines) -> AzureOCREngine:
    return engines.azure()


@pytest.fixture
def azure_engine_mock(engines, mocker):
    mock = mocker.Mock(engines.azure.cls)
    with engines.azure.override(mock):
        yield mock


@pytest.fixture
def tesseract_engine_mock(engines, mocker):
    mock = mocker.Mock(engines.tesseract.cls)
    with engines.tesseract.override(mock):
        yield mock


@pytest.fixture
def easy_ocr_engine_mock(engines, mocker):
    mock = mocker.Mock(engines.easy_ocr.cls)
    with engines.easy_ocr.override(mock):
        yield mock


@pytest.fixture
def craft_tesseract_engine_mock(engines, mocker):
    mock = mocker.Mock(engines.craft_tesseract.cls)
    with engines.craft_tesseract.override(mock):
        yield mock


@pytest.fixture
def paddle_ocr_engine_mock(engines, mocker):
    mock = mocker.Mock(engines.paddle_ocr.cls)
    with engines.paddle_ocr.override(mock):
        yield mock


@pytest.fixture
def reference_layout_deleted_envelope(mocker, document_layout_id):
    dee = mocker.Mock(DomainEventEnvelope)
    dee.event.reference_layout_id = document_layout_id
    return dee


@pytest.fixture
def document_deleted_envelope(mocker, document_layout_id):
    dee = mocker.Mock(DomainEventEnvelope)
    dee.event.document_id = document_layout_id
    return dee


@pytest.fixture
def file_deleted_envelope(mocker, document_layout_id, faker):
    dee = mocker.Mock(DomainEventEnvelope)
    dee.event = FileDeleted(id=document_layout_id, path=faker.file_path())

    return dee


@pytest.fixture
def test_saved_full_document_layout(document_layout_repository, tenant_id):
    copied_dl = deepcopy(full_document_layout)
    copied_dl.__dict__["_tenant_id"].__dict__["_value"] = tenant_id
    document_layout_repository.save(copied_dl)
    return copied_dl


@pytest.fixture
def test_saved_full_tabular_layout(fake_tl_command_repository, tenant_id) -> TabularLayout:
    copied_tl = deepcopy(full_tabular_layout)
    copied_tl.__dict__["_tenant_id"].__dict__["_value"] = tenant_id
    fake_tl_command_repository.save(copied_tl)
    return copied_tl


@pytest.fixture(autouse=True)
def mocked_middleware(monkeypatch, mocker):
    monkeypatch.setattr(api.auth, "set_user_from_token", mocker.Mock({}))


@pytest.fixture
def empty_tabular_layout() -> TabularLayout:
    return TabularLayoutFactory.make_empty_layout(
        document_id="document_id",
        tenant_id="tenant_id",
        parsing_type=TLParsingType.EXCEL,
    )


@pytest.fixture
def ocr_image_processing_service(containers) -> OCRLayoutImageProcessingService:
    return containers.applications.ocr_image_preprocessing_service()


@pytest.fixture
def save_content_to_storage(fake_file_storage_proxy: ObjectStorage, file_path: str, faker: Faker) -> None:
    fake_file_storage_proxy.upload(path=file_path, content=faker.binary(length=64), replace_if_exists=True)
