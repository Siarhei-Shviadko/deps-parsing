from copy import deepcopy
from uuid import uuid4

import pytest
from deps_document_layout.model import (
    DocumentLayout,
    DocumentLayoutFactory,
    EntityId,
    PageBatch,
    TenantId,
)
from deps_tabular_layout.models import ParsingType, TabularLayout, TabularLayoutFactory
from faker.proxy import Faker
from fastapi import FastAPI
from pytest_factoryboy import register
from starlette.testclient import TestClient

from deps_parsing.application import TabularLayoutService
from deps_parsing.domain.model import CommandChannel, DocumentType
from deps_parsing.entrypoint import create_fastapi
from deps_parsing.infrastructure.access_management import user
from deps_parsing.infrastructure.dl_parsing import (
    AWSTextractParsingStrategyEnum,
    AzureParsingStrategyEnum,
    GCPDocumentAIParsingStrategyEnum,
)
from deps_parsing.infrastructure.repositories.document_layout.mappers import (
    DocumentLayoutMapper,
)
from tests import factories
from tests.fakes import (
    FakeAWSTextractProxy,
    FakeAzureProxy,
    FakeCommandProducer,
    FakeDocumentAIProxy,
    FakeDomainEventPublisher,
    FakeUnifierProxy,
)


@pytest.fixture(scope="session")
def app() -> FastAPI:
    fastapi_app = create_fastapi()
    yield fastapi_app


@pytest.fixture
def client(app):
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="session")
def session_containers(app):
    return app.containers


@pytest.fixture
def containers(session_containers):
    with session_containers.reset_singletons():
        yield session_containers


@pytest.fixture
def config(containers):
    yield containers.config


@pytest.fixture
def repositories(containers):
    return containers.repositories


@pytest.fixture
def external_services(containers):
    return containers.external_services


@pytest.fixture
def engines(containers):
    return containers.engines


@pytest.fixture
def domain_services(containers):
    return containers.domain_services


@pytest.fixture
def split_tables_detection_service(domain_services):
    return domain_services.split_tables_detector()


@pytest.fixture
def test_command_channel():
    return CommandChannel("test_command_channel")


@pytest.fixture
def deps_token(tenant_id):
    return {
        "organisation": tenant_id,
        "subject": "subject",
        "roles": [],
        "groups": [tenant_id],
    }


@pytest.fixture(autouse=True)
def set_user(deps_token):
    token = user.set(deps_token)
    yield
    user.reset(token)


@pytest.fixture(autouse=True)
def fake_domain_event_publisher(containers):
    with containers.domain_event_publisher.override(FakeDomainEventPublisher()) as dep:
        yield dep()


@pytest.fixture
def fake_command_producer(containers):
    with containers.command_producer.override(FakeCommandProducer()) as cp:
        yield cp()


@pytest.fixture
def fake_unifier_proxy(external_services):
    with external_services.unifier.override(FakeUnifierProxy()) as up:
        yield up()


@pytest.fixture
def fake_azure_proxy(external_services):
    with external_services.azure.override(FakeAzureProxy()) as fap:
        yield fap()


@pytest.fixture
def fake_aws_textract_proxy(external_services):
    with external_services.aws_textract.override(FakeAWSTextractProxy()) as fap:
        yield fap()


@pytest.fixture
def fake_gcp_document_ai_proxy(external_services):
    with external_services.gcp_document_ai.override(FakeDocumentAIProxy()) as fap:
        yield fap()


@pytest.fixture
def tenant_id():
    return uuid4().hex


@pytest.fixture
def document_id():
    return uuid4().hex


@pytest.fixture
def entity_id():
    return uuid4().hex


@pytest.fixture
def file_path(faker: Faker):
    return faker.file_path()


@pytest.fixture
def document_layout_id():
    return uuid4().hex


@pytest.fixture
def table_id():
    return uuid4().hex


@pytest.fixture
def default_page_batch():
    return PageBatch()


@pytest.fixture
def document_layout(tenant_id, document_layout_id) -> DocumentLayout:
    return DocumentLayoutFactory.make_document_layout(id_=document_layout_id, tenant_id=tenant_id)


@pytest.fixture
def document_layout_dict(document_layout):
    return DocumentLayoutMapper.to_dict(document_layout)


@pytest.fixture
def test_tabular_layout(document_layout_id, tenant_id) -> TabularLayout:
    tl = TabularLayoutFactory.make_empty_layout(
        document_id=document_layout_id,
        tenant_id=tenant_id,
        parsing_type=ParsingType.EXCEL,
        extracted_props=[],
    )
    return tl


@pytest.fixture
def saved_test_tabular_layout(repositories, test_tabular_layout) -> TabularLayout:
    repo = repositories.tabular_layout_command()
    repo.save(test_tabular_layout)
    return test_tabular_layout


@pytest.fixture
def test_document_type(test_command_channel, tenant_id):
    return DocumentType(EntityId(uuid4().hex), TenantId(tenant_id), test_command_channel)


@pytest.fixture
def tabular_layout_service(containers) -> TabularLayoutService:
    return containers.applications.tabular_layout_service()


@pytest.fixture
def set_by_page_strategy(containers):
    config = deepcopy(containers.config())
    config["azure_dl_parsing"]["parsing_strategy"] = AzureParsingStrategyEnum.BY_PAGE
    config["aws_textract"]["parsing_strategy"] = AWSTextractParsingStrategyEnum.BY_PAGE
    config["gcp_document_ai"]["parsing_strategy"] = GCPDocumentAIParsingStrategyEnum.BY_PAGE

    with containers.config.override(config):
        yield


@pytest.fixture
def set_by_document_strategy(containers):
    config = deepcopy(containers.config())
    config["azure_dl_parsing"]["parsing_strategy"] = AzureParsingStrategyEnum.BY_DOCUMENT
    config["aws_textract"]["parsing_strategy"] = AWSTextractParsingStrategyEnum.BY_DOCUMENT
    config["gcp_document_ai"]["parsing_strategy"] = GCPDocumentAIParsingStrategyEnum.BY_DOCUMENT

    with containers.config.override(config):
        yield


@pytest.fixture
def docx_file_with_paragraph_and_table() -> bytes:
    file_path = "tests/data/docx/with_paragraph_and_table.docx"
    with open(file_path, "rb") as docx_file:
        return docx_file.read()


@pytest.fixture
def excel_file_all_styles() -> bytes:
    with open("tests/data/excel/1-sheet-large-table.xlsx", "rb") as file:
        return file.read()


@pytest.fixture
def csv_base_file():
    with open("./tests/data/csv/base.csv", "rb") as f:
        return f.read()


for factory in [f for _, f in factories.__dict__.items() if callable(f)]:
    register(factory)
