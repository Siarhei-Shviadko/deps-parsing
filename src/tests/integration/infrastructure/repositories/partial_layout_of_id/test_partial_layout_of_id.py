import pytest
from deps_document_layout.model import LayoutWishList, PageWishList, ParsingType
from more_itertools import first, nth

from tests.helpers import full_compare_2_document_layouts


@pytest.mark.partial
def test_get_layout__no_layout__none(document_layout_repository, document_layout):
    layout = document_layout_repository.partial_layout_of_id(
        layout_id=document_layout.id(),
        tenant_id=document_layout.tenant_id(),
        wish_list=LayoutWishList(parsing_type=ParsingType.AWS_TEXTRACT),
    )

    assert layout is None


@pytest.mark.partial
@pytest.mark.usefixtures("save_document_layout")
def test_get_layout__empty_wish_list__full_document_layout(document_layout_repository, document_layout):
    layout = document_layout_repository.partial_layout_of_id(
        layout_id=document_layout.id(),
        tenant_id=document_layout.tenant_id(),
        wish_list=LayoutWishList(parsing_type=ParsingType.AWS_TEXTRACT),
    )

    assert len(layout.pages) == len(document_layout.pages)
    full_compare_2_document_layouts(layout_1=layout, layout_2=document_layout)


@pytest.mark.partial
@pytest.mark.usefixtures("save_document_layout")
def test_get_layout__page_id_given__only_requested_pages(document_layout_repository, document_layout, page1_id):
    pages = [PageWishList(page_id=page1_id())]

    layout = document_layout_repository.partial_layout_of_id(
        layout_id=document_layout.id(),
        tenant_id=document_layout.tenant_id(),
        wish_list=LayoutWishList(pages=pages, parsing_type=ParsingType.AWS_TEXTRACT),
    )

    assert len(layout.pages) == len(pages)
    full_compare_2_document_layouts(layout_1=layout, layout_2=document_layout)


@pytest.mark.partial
@pytest.mark.usefixtures("save_document_layout")
def test_partial_layout_of_id__one_image_id__one_image(
    document_layout_repository,
    page1_image1_id,
    document_layout,
    page1_id,
):
    layout = document_layout_repository.partial_layout_of_id(
        layout_id=document_layout.id(),
        tenant_id=document_layout.tenant_id(),
        wish_list=LayoutWishList(
            pages=[PageWishList(page_id=page1_id(), image_ids=[page1_image1_id()])],
            parsing_type=ParsingType.AWS_TEXTRACT,
        ),
    )

    assert len(pages := layout.pages) == 1
    assert (page := first(pages)).id == page1_id
    assert len(images := page.images) == 1
    assert first(images).id == page1_image1_id


@pytest.mark.partial
@pytest.mark.usefixtures("save_document_layout")
def test_partial_layout_of_id__two_image_ids__one_page_two_images(
    document_layout_repository,
    page1_image1_id,
    page1_image2_id,
    document_layout,
    page1_id,
):
    layout = document_layout_repository.partial_layout_of_id(
        layout_id=document_layout.id(),
        tenant_id=document_layout.tenant_id(),
        wish_list=LayoutWishList(
            pages=[PageWishList(page_id=page1_id(), image_ids=[page1_image1_id(), page1_image2_id()])],
            parsing_type=ParsingType.AWS_TEXTRACT,
        ),
    )

    assert len(pages := layout.pages) == 1
    assert len(images := first(pages).images) == 2
    assert first(images).id == page1_image1_id
    assert nth(images, n=1).id == page1_image2_id


@pytest.mark.partial
@pytest.mark.usefixtures("save_document_layout")
def test_partial_layout_of_id__two_pages_ids_three_image_ids__two_pages_three_images(
    document_layout_repository,
    page1_image1_id,
    page2_image1_id,
    page2_image2_id,
    document_layout,
    page1_id,
    page2_id,
):
    layout = document_layout_repository.partial_layout_of_id(
        layout_id=document_layout.id(),
        tenant_id=document_layout.tenant_id(),
        wish_list=LayoutWishList(
            pages=[
                PageWishList(page_id=page1_id(), image_ids=[page1_image1_id()]),
                PageWishList(page_id=page2_id(), image_ids=[page2_image1_id(), page2_image2_id()]),
            ],
            parsing_type=ParsingType.AWS_TEXTRACT,
        ),
    )

    assert len(pages := layout.pages) == 2
    assert (page1 := first(pages)).id == page1_id
    assert (page2 := nth(pages, n=1)).id == page2_id
    assert len(page1_images := page1.images) == 1
    assert len(page2_images := page2.images) == 2
    assert first(page1_images).id == page1_image1_id
    assert first(page2_images).id == page2_image1_id
    assert nth(page2_images, n=1).id == page2_image2_id
    assert not page1.paragraphs
    assert not page1.key_value_pairs
    assert not page1.tables
    assert not page2.paragraphs
    assert not page2.key_value_pairs
    assert not page2.tables


@pytest.mark.partial
@pytest.mark.usefixtures("save_document_layout")
def test_partial_layout_of_id__one_paragraph_id__one_paragraph(
    document_layout_repository,
    document_layout,
    page1_id,
    page1_paragraph1_id,
):
    layout = document_layout_repository.partial_layout_of_id(
        layout_id=document_layout.id(),
        tenant_id=document_layout.tenant_id(),
        wish_list=LayoutWishList(
            pages=[PageWishList(page_id=page1_id(), paragraph_ids=[page1_paragraph1_id()])],
            parsing_type=ParsingType.AWS_TEXTRACT,
        ),
    )

    assert len(pages := layout.pages) == 1
    assert (page := first(pages)).id == page1_id
    assert len(paragraphs := page.paragraphs) == 1
    assert first(paragraphs).id == page1_paragraph1_id


@pytest.mark.partial
@pytest.mark.usefixtures("save_document_layout")
def test_partial_layout_of_id__two_paragraph_ids__one_page_two_paragraphs(
    document_layout_repository,
    page1_paragraph1_id,
    page1_paragraph2_id,
    document_layout,
    page1_id,
):
    layout = document_layout_repository.partial_layout_of_id(
        layout_id=document_layout.id(),
        tenant_id=document_layout.tenant_id(),
        wish_list=LayoutWishList(
            pages=[PageWishList(page_id=page1_id(), paragraph_ids=[page1_paragraph1_id(), page1_paragraph2_id()])],
            parsing_type=ParsingType.AWS_TEXTRACT,
        ),
    )

    assert len(pages := layout.pages) == 1
    assert (page := first(pages)).id == page1_id
    assert len(paragraphs := page.paragraphs) == 2
    assert first(paragraphs).id == page1_paragraph1_id
    assert nth(paragraphs, n=1).id == page1_paragraph2_id


@pytest.mark.partial
@pytest.mark.usefixtures("save_document_layout")
def test_partial_layout_of_id__two_pages_ids_three_paragraphs_ids__two_pages_three_paragraphs(
    document_layout_repository,
    page1_paragraph1_id,
    page2_paragraph1_id,
    page2_paragraph2_id,
    document_layout,
    page1_id,
    page2_id,
):
    layout = document_layout_repository.partial_layout_of_id(
        layout_id=document_layout.id(),
        tenant_id=document_layout.tenant_id(),
        wish_list=LayoutWishList(
            pages=[
                PageWishList(page_id=page1_id(), paragraph_ids=[page1_paragraph1_id()]),
                PageWishList(page_id=page2_id(), paragraph_ids=[page2_paragraph1_id(), page2_paragraph2_id()]),
            ],
            parsing_type=ParsingType.AWS_TEXTRACT,
        ),
    )

    assert len(pages := layout.pages) == 2
    assert (page1 := first(pages)).id == page1_id
    assert (page2 := nth(pages, n=1)).id == page2_id
    assert len(page1_paragraphs := page1.paragraphs) == 1
    assert len(page2_paragraphs := page2.paragraphs) == 2
    assert first(page1_paragraphs).id == page1_paragraph1_id
    assert first(page2_paragraphs).id == page2_paragraph1_id
    assert nth(page2_paragraphs, n=1).id == page2_paragraph2_id
    assert not page1.images
    assert not page1.key_value_pairs
    assert not page1.tables
    assert not page2.images
    assert not page2.key_value_pairs
    assert not page2.tables


@pytest.mark.partial
@pytest.mark.usefixtures("save_document_layout")
def test_partial_layout_of_id__one_table_id__one_table_all_paragraphs(
    document_layout_repository,
    page1_table1_id,
    document_layout,
    page1_id,
):
    layout = document_layout_repository.partial_layout_of_id(
        layout_id=document_layout.id(),
        tenant_id=document_layout.tenant_id(),
        wish_list=LayoutWishList(
            pages=[PageWishList(page_id=page1_id(), table_ids=[page1_table1_id()])],
            parsing_type=ParsingType.AWS_TEXTRACT,
        ),
    )

    assert len(pages := layout.pages) == 1
    assert (page := first(pages)).id == page1_id
    assert len(tables := page.tables) == 1
    assert first(tables).id == page1_table1_id
    assert len(page.paragraphs) == len(first(document_layout.pages).paragraphs)


@pytest.mark.partial
@pytest.mark.usefixtures("save_document_layout")
def test_partial_layout_of_id__two_table_ids__one_page_two_tables(
    document_layout_repository,
    page1_table1_id,
    page1_table2_id,
    document_layout,
    page1_id,
):
    layout = document_layout_repository.partial_layout_of_id(
        layout_id=document_layout.id(),
        tenant_id=document_layout.tenant_id(),
        wish_list=LayoutWishList(
            pages=[PageWishList(page_id=page1_id(), table_ids=[page1_table1_id(), page1_table2_id()])],
            parsing_type=ParsingType.AWS_TEXTRACT,
        ),
    )

    assert len(pages := layout.pages) == 1
    assert len(tables := first(pages).tables) == 2
    assert first(tables).id == page1_table1_id
    assert nth(tables, n=1).id == page1_table2_id


@pytest.mark.partial
@pytest.mark.usefixtures("save_document_layout")
def test_partial_layout_of_id__two_pages_ids_three_table_ids__two_pages_three_tables(
    document_layout_repository,
    page1_table1_id,
    page2_table1_id,
    page2_table2_id,
    document_layout,
    page1_id,
    page2_id,
):
    layout = document_layout_repository.partial_layout_of_id(
        layout_id=document_layout.id(),
        tenant_id=document_layout.tenant_id(),
        wish_list=LayoutWishList(
            pages=[
                PageWishList(page_id=page1_id(), table_ids=[page1_table1_id()]),
                PageWishList(page_id=page2_id(), table_ids=[page2_table1_id(), page2_table2_id()]),
            ],
            parsing_type=ParsingType.AWS_TEXTRACT,
        ),
    )

    assert len(pages := layout.pages) == 2
    assert (page1 := first(pages)).id == page1_id
    assert (page2 := nth(pages, n=1)).id == page2_id
    assert len(page1_tables := page1.tables) == 1
    assert len(page2_tables := page2.tables) == 2
    assert first(page1_tables).id == page1_table1_id
    assert first(page2_tables).id == page2_table1_id
    assert nth(page2_tables, n=1).id == page2_table2_id
    assert len(page1.paragraphs) == len(first(document_layout.pages).paragraphs)
    assert not page1.key_value_pairs
    assert not page1.images
    assert len(page2.paragraphs) == len(nth(document_layout.pages, n=1).paragraphs)
    assert not page2.key_value_pairs
    assert not page2.images


@pytest.mark.partial
@pytest.mark.usefixtures("save_document_layout")
def test_partial_layout_of_id__one_kvp_id__one_kvp_all_paragraphs(
    document_layout_repository,
    page1_kvp1_id,
    document_layout,
    page1_id,
):
    layout = document_layout_repository.partial_layout_of_id(
        layout_id=document_layout.id(),
        tenant_id=document_layout.tenant_id(),
        wish_list=LayoutWishList(
            pages=[PageWishList(page_id=page1_id(), key_value_pair_ids=[page1_kvp1_id()])],
            parsing_type=ParsingType.AWS_TEXTRACT,
        ),
    )

    assert len(pages := layout.pages) == 1
    assert (page := first(pages)).id == page1_id
    assert len(key_value_pairs := page.key_value_pairs) == 1
    assert first(key_value_pairs).id == page1_kvp1_id
    assert len(page.paragraphs) == len(first(document_layout.pages).paragraphs)


@pytest.mark.partial
@pytest.mark.usefixtures("save_document_layout")
def test_partial_layout_of_id__two_kvp_ids__one_page_two_kvps(
    document_layout_repository,
    page1_kvp1_id,
    page1_kvp2_id,
    document_layout,
    page1_id,
):
    layout = document_layout_repository.partial_layout_of_id(
        layout_id=document_layout.id(),
        tenant_id=document_layout.tenant_id(),
        wish_list=LayoutWishList(
            pages=[PageWishList(page_id=page1_id(), key_value_pair_ids=[page1_kvp1_id(), page1_kvp2_id()])],
            parsing_type=ParsingType.AWS_TEXTRACT,
        ),
    )

    assert len(pages := layout.pages) == 1
    assert len(key_value_pairs := first(pages).key_value_pairs) == 2
    assert first(key_value_pairs).id == page1_kvp1_id
    assert nth(key_value_pairs, n=1).id == page1_kvp2_id


@pytest.mark.partial
@pytest.mark.usefixtures("save_document_layout")
def test_partial_layout_of_id__two_pages_ids_three_kvp_ids__two_pages_three_kvps(
    document_layout_repository,
    page1_kvp1_id,
    page2_kvp1_id,
    page2_kvp2_id,
    document_layout,
    page1_id,
    page2_id,
):
    layout = document_layout_repository.partial_layout_of_id(
        layout_id=document_layout.id(),
        tenant_id=document_layout.tenant_id(),
        wish_list=LayoutWishList(
            pages=[
                PageWishList(page_id=page1_id(), key_value_pair_ids=[page1_kvp1_id()]),
                PageWishList(page_id=page2_id(), key_value_pair_ids=[page2_kvp1_id(), page2_kvp2_id()]),
            ],
            parsing_type=ParsingType.AWS_TEXTRACT,
        ),
    )

    assert len(pages := layout.pages) == 2
    assert (page1 := first(pages)).id == page1_id
    assert (page2 := nth(pages, n=1)).id == page2_id
    assert len(page1_key_value_pairs := page1.key_value_pairs) == 1
    assert len(page2_key_value_pairs := page2.key_value_pairs) == 2
    assert first(page1_key_value_pairs).id == page1_kvp1_id
    assert first(page2_key_value_pairs).id == page2_kvp1_id
    assert nth(page2_key_value_pairs, n=1).id == page2_kvp2_id
    assert len(page1.paragraphs) == len(first(document_layout.pages).paragraphs)
    assert not page1.tables
    assert not page1.images
    assert len(page2.paragraphs) == len(nth(document_layout.pages, n=1).paragraphs)
    assert not page2.tables
    assert not page2.images


@pytest.mark.partial
@pytest.mark.usefixtures("save_document_layout")
def test_partial_layout_of_id__all_features_by_one__ok(
    document_layout_repository,
    page1_kvp1_id,
    page1_paragraph1_id,
    page1_table1_id,
    page1_image1_id,
    document_layout,
    page1_id,
):
    layout = document_layout_repository.partial_layout_of_id(
        layout_id=document_layout.id(),
        tenant_id=document_layout.tenant_id(),
        wish_list=LayoutWishList(
            pages=[
                PageWishList(
                    page_id=page1_id(),
                    key_value_pair_ids=[page1_kvp1_id()],
                    paragraph_ids=[page1_paragraph1_id()],
                    table_ids=[page1_table1_id()],
                    image_ids=[page1_image1_id()],
                ),
            ],
            parsing_type=ParsingType.AWS_TEXTRACT,
        ),
    )

    assert len(pages := layout.pages) == 1
    assert (page := first(pages)).id == page1_id
    assert len(page.paragraphs) == len(first(document_layout.pages).paragraphs)
    assert len(key_value_pairs := page.key_value_pairs) == 1
    assert first(key_value_pairs).id == page1_kvp1_id
    assert len(tables := page.tables) == 1
    assert first(tables).id == page1_table1_id
    assert len(images := page.images) == 1
    assert first(images).id == page1_image1_id


@pytest.mark.partial
@pytest.mark.usefixtures("save_document_layout")
def test_partial_layout_of_id__all_features_by_one_different_parsing_type__no_pages(
    document_layout_repository,
    page1_kvp1_id,
    page1_paragraph1_id,
    page1_table1_id,
    page1_image1_id,
    document_layout,
    page1_id,
):
    layout = document_layout_repository.partial_layout_of_id(
        layout_id=document_layout.id(),
        tenant_id=document_layout.tenant_id(),
        wish_list=LayoutWishList(
            pages=[
                PageWishList(
                    page_id=page1_id(),
                    key_value_pair_ids=[page1_kvp1_id()],
                    paragraph_ids=[page1_paragraph1_id()],
                    table_ids=[page1_table1_id()],
                    image_ids=[page1_image1_id()],
                ),
            ],
            parsing_type=ParsingType.TESSERACT,
        ),
    )

    assert not layout.pages
