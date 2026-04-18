import pytest
from deps_document_layout.model import DocumentLayout, EntityId, Page, ParsingType
from more_itertools import first, nth

__all__ = [
    "page1_id",
    "page2_id",
    "page3_id",
    "document_layout",
    "page1",
    "page2",
    "page1_image1_id",
    "page1_image2_id",
    "page2_image1_id",
    "page2_image2_id",
    "page1_paragraph1_id",
    "page1_paragraph2_id",
    "page2_paragraph1_id",
    "page2_paragraph2_id",
    "page1_table1_id",
    "page1_table2_id",
    "page2_table1_id",
    "page2_table2_id",
    "page1_kvp1_id",
    "page1_kvp2_id",
    "page2_kvp1_id",
    "page2_kvp2_id",
]


@pytest.fixture
def page1_id() -> EntityId:
    return EntityId()


@pytest.fixture
def page2_id() -> EntityId:
    return EntityId()


@pytest.fixture
def page3_id() -> EntityId:
    return EntityId()


@pytest.fixture
def document_layout(
    document_layout,
    page_factory,
    image_factory,
    key_value_pair_factory,
    paragraph_factory,
    table_factory,
    page1_id,
    page2_id,
    page3_id,
) -> DocumentLayout:
    document_layout.pages.extend(
        page_factory(
            id_=page_id,
            parsing_type=ParsingType.AWS_TEXTRACT,
            images=tuple(image_factory() for _ in range(3)),
            key_value_pairs=tuple(key_value_pair_factory() for _ in range(3)),
            paragraphs=tuple(paragraph_factory() for _ in range(3)),
            tables=tuple(table_factory() for _ in range(3)),
        )
        for page_id in (page1_id, page2_id, page3_id)
    )

    return document_layout


@pytest.fixture
def page1(document_layout) -> Page:
    return first(document_layout.pages)


@pytest.fixture
def page2(document_layout) -> Page:
    return nth(document_layout.pages, n=1)


@pytest.fixture
def page1_image1_id(page1) -> EntityId:
    return first(page1.images).id


@pytest.fixture
def page1_image2_id(page1) -> EntityId:
    return nth(page1.images, n=1).id


@pytest.fixture
def page2_image1_id(page2) -> EntityId:
    return first(page2.images).id


@pytest.fixture
def page2_image2_id(page2) -> EntityId:
    return nth(page2.images, n=1).id


@pytest.fixture
def page1_paragraph1_id(page1) -> EntityId:
    return first(page1.paragraphs).id


@pytest.fixture
def page1_paragraph2_id(page1) -> EntityId:
    return nth(page1.paragraphs, n=1).id


@pytest.fixture
def page2_paragraph1_id(page2) -> EntityId:
    return first(page2.paragraphs).id


@pytest.fixture
def page2_paragraph2_id(page2) -> EntityId:
    return nth(page2.paragraphs, n=1).id


@pytest.fixture
def page1_table1_id(page1) -> EntityId:
    return first(page1.tables).id


@pytest.fixture
def page1_table2_id(page1) -> EntityId:
    return nth(page1.tables, n=1).id


@pytest.fixture
def page2_table1_id(page2) -> EntityId:
    return first(page2.tables).id


@pytest.fixture
def page2_table2_id(page2) -> EntityId:
    return nth(page2.tables, n=1).id


@pytest.fixture
def page1_kvp1_id(page1) -> EntityId:
    return first(page1.key_value_pairs).id


@pytest.fixture
def page1_kvp2_id(page1) -> EntityId:
    return nth(page1.key_value_pairs, n=1).id


@pytest.fixture
def page2_kvp1_id(page2) -> EntityId:
    return first(page2.key_value_pairs).id


@pytest.fixture
def page2_kvp2_id(page2) -> EntityId:
    return nth(page2.key_value_pairs, n=1).id
