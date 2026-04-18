from typing import Any
from uuid import uuid4

import pytest
from deps_document_layout.model import (
    CellUpdateData,
    EntityId,
    LineUpdateData,
    ParsingFeature,
    ParsingType,
    RawPoint,
    RawPolygon,
    TenantId,
)
from faker.proxy import Faker

from deps_parsing.domain.model import DocumentType


@pytest.fixture
def test_document_type_without_command_channel(tenant_id):
    return DocumentType(EntityId(uuid4().hex), TenantId(tenant_id))


@pytest.fixture
def paragraph_update_data(faker: Faker, polygon_factory) -> list[LineUpdateData]:
    return [
        LineUpdateData(content=faker.text(max_nb_chars=30), polygon=polygon_factory(), order=0),
        LineUpdateData(content=faker.text(max_nb_chars=30), polygon=polygon_factory(), order=1),
        LineUpdateData(content=faker.text(max_nb_chars=30), polygon=polygon_factory(), order=2),
    ]


@pytest.fixture
def image_update_data(faker: Faker, polygon_factory) -> dict[str, Any]:
    return {
        "title": faker.text(max_nb_chars=30),
        "description": faker.text(max_nb_chars=100),
        "polygon": RawPolygon(tuple(RawPoint(x=p.x, y=p.y) for p in polygon_factory())),
        "filepath": faker.file_path(depth=1, extension="jpg"),
    }


@pytest.fixture
def table_update_data(faker: Faker) -> list[CellUpdateData]:
    return [
        CellUpdateData(content=faker.text(max_nb_chars=30), row_index=0, column_index=0),
        CellUpdateData(content=faker.text(max_nb_chars=30), row_index=0, column_index=1),
        CellUpdateData(content=faker.text(max_nb_chars=30), row_index=0, column_index=2),
    ]


@pytest.fixture
def saved_layout_with_user_defined_pages(
    test_saved_full_document_layout,
    document_layout_repository,
    document_layout_service,
):
    test_saved_full_document_layout.parsing_features.update({ParsingType.AWS_TEXTRACT: set(ParsingFeature)})
    document_layout_repository.save(test_saved_full_document_layout)

    test_saved_full_document_layout.clone_pages_with_new_parsing_type(
        original_parsing_type=ParsingType.AWS_TEXTRACT,
        new_parsing_type=ParsingType.USER_DEFINED,
    )

    document_layout_repository.save_cloned_user_defined_document_layout(test_saved_full_document_layout)

    return test_saved_full_document_layout
