import pytest
from deps_document_layout.model import (
    DocumentLayout,
    DocumentLayoutFactory,
    EntityId,
    ParsingType,
)

__all__ = [
    "layout",
    "save_layout",
    "user_defined_parsing_type",
    "page_id",
    "paragraph_id",
    "paragraph2_id",
    "paragraph3_id",
    "table_id",
    "key_value_pair_id",
    "image_id",
]


@pytest.fixture
def user_defined_parsing_type() -> ParsingType:
    return ParsingType.USER_DEFINED


@pytest.fixture
def page_id() -> EntityId:
    return EntityId()


@pytest.fixture
def paragraph_id() -> EntityId:
    return EntityId()


@pytest.fixture
def image_id() -> EntityId:
    return EntityId()


@pytest.fixture
def paragraph2_id() -> EntityId:
    return EntityId()


@pytest.fixture
def paragraph3_id() -> EntityId:
    return EntityId()


@pytest.fixture
def table_id() -> EntityId:
    return EntityId()


@pytest.fixture
def key_value_pair_id() -> EntityId:
    return EntityId()


@pytest.fixture
def layout(
    user_defined_parsing_type,
    document_layout_id,
    paragraph_factory,
    image_factory,
    table_factory,
    paragraph2_id,
    paragraph3_id,
    paragraph_id,
    cell_factory,
    line_factory,
    page_factory,
    tenant_id,
    page_id,
    image_id,
    table_id,
    key_value_pair_factory,
    key_value_pair_id,
) -> DocumentLayout:
    layout = DocumentLayoutFactory.make_document_layout(tenant_id=tenant_id, id_=document_layout_id)
    layout.pages.append(
        page_factory(
            id_=page_id,
            parsing_type=user_defined_parsing_type,
            paragraphs=(
                paragraph_factory(id_=paragraph_id, lines=tuple(line_factory(order=order) for order in range(3))),
                paragraph_factory(id_=paragraph2_id, lines=tuple(line_factory(order=order) for order in range(3))),
                paragraph_factory(id_=paragraph3_id, lines=tuple(line_factory(order=order) for order in range(3))),
            ),
            tables=(
                table_factory(
                    id_=table_id,
                    cells=(
                        cell_factory(row_index=0, column_index=0, paragraph_id=paragraph_id),
                        cell_factory(row_index=0, column_index=1, paragraph_id=paragraph2_id),
                        cell_factory(row_index=0, column_index=2, paragraph_id=paragraph3_id),
                    ),
                ),
            ),
            images=(image_factory(id_=image_id),),
            key_value_pairs=(key_value_pair_factory(id_=key_value_pair_id),),
        ),
    )
    return layout


@pytest.fixture
def save_layout(layout, document_layout_repository) -> None:
    document_layout_repository.save(layout)
