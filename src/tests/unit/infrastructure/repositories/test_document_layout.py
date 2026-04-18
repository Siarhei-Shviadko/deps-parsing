from deps_document_layout.model.document_layout import (
    DocumentLayoutFeaturesFilter,
    ParsingType,
)

from deps_parsing.infrastructure.repositories import DocumentLayoutRepository
from tests.data.document_layout import (
    document_layout_user_defined,
    document_layout_user_defined_2,
)

FIRST_ELEMENT = 0
SECOND_ELEMENT = 1


def test_save_cloned_user_defined_document_layout__ok(document_layout_repository: DocumentLayoutRepository):
    document_layout_repository.save(document_layout_user_defined)
    document_layout_repository.save_cloned_user_defined_document_layout(document_layout_user_defined_2)

    saved_document_layout = document_layout_repository.layout_of_id(
        layout_id=document_layout_user_defined.id(),
        tenant_id=document_layout_user_defined.tenant_id(),
        filtering=DocumentLayoutFeaturesFilter(
            parsing_type=ParsingType.USER_DEFINED,
            features=set(),
        ),
    )

    assert saved_document_layout.id == document_layout_user_defined.id
    assert saved_document_layout.tenant_id == document_layout_user_defined.tenant_id
    assert saved_document_layout.pages[FIRST_ELEMENT] != document_layout_user_defined.pages[FIRST_ELEMENT]
    assert saved_document_layout.pages[FIRST_ELEMENT] == document_layout_user_defined_2.pages[FIRST_ELEMENT]


def test_save_cloned_user_defined_document_layout__no_layout__no_error(
    document_layout_repository: DocumentLayoutRepository,
):
    document_layout_repository.save_cloned_user_defined_document_layout(document_layout_user_defined_2)

    saved_document_layout = document_layout_repository.layout_of_id(
        layout_id=document_layout_user_defined_2.id(),
        tenant_id=document_layout_user_defined_2.tenant_id(),
        filtering=DocumentLayoutFeaturesFilter(
            parsing_type=ParsingType.USER_DEFINED,
            features=set(),
        ),
    )

    assert saved_document_layout.id == document_layout_user_defined_2.id
    assert saved_document_layout.tenant_id == document_layout_user_defined_2.tenant_id
    assert saved_document_layout.pages == document_layout_user_defined_2.pages
