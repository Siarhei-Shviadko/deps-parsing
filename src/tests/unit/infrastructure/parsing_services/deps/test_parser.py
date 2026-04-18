from deps_document_layout.model import ParsingType

from deps_parsing.infrastructure.dl_parsing import DepsParser, DepsStructuredResponse
from tests.data.deps import ocr_response_, tables_response_


def test_deps_parser__only_ocr__ok(unified_data_image_page1, document_layout):
    response = DepsStructuredResponse(dict(ocr_data=ocr_response_, tables_data=None))
    layout = DepsParser(unified_data_image_page1, ParsingType.TESSERACT).add_response_to_page(response, document_layout)

    assert len(layout.pages) == 1
    assert len(layout.pages[0].paragraphs) == 1
    assert layout.pages[0].id() == unified_data_image_page1.id
    assert layout.pages[0].dimension.width == unified_data_image_page1.width
    assert layout.pages[0].dimension.height == unified_data_image_page1.height
    assert layout.pages[0].dimension.unit == "px"
    assert (
        layout.pages[0].transformations.angle
        == unified_data_image_page1.applied_transformation.parameters.kwargs["angle"]
    )
    assert (
        layout.pages[0].transformations.orientation
        == unified_data_image_page1.applied_transformation.parameters.kwargs["orientation"]
    )


def test_deps_parser__only_tables__ok(unified_data_image_page1, document_layout):
    response = DepsStructuredResponse(dict(ocr_data=[], tables_data=tables_response_))
    layout = DepsParser(unified_data_image_page1, ParsingType.TESSERACT).add_response_to_page(response, document_layout)

    assert len(layout.pages) == 1
    assert len(layout.pages[0].tables) == 1
    assert layout.pages[0].id() == unified_data_image_page1.id
    assert layout.pages[0].dimension.width == unified_data_image_page1.width
    assert layout.pages[0].dimension.height == unified_data_image_page1.height
    assert layout.pages[0].dimension.unit == "px"
    assert (
        layout.pages[0].transformations.angle
        == unified_data_image_page1.applied_transformation.parameters.kwargs["angle"]
    )
    assert (
        layout.pages[0].transformations.orientation
        == unified_data_image_page1.applied_transformation.parameters.kwargs["orientation"]
    )


def test_deps_parser__ocr_and_tables__ok(unified_data_image_page1, document_layout):
    response = DepsStructuredResponse(
        dict(
            ocr_data=ocr_response_,
            tables_data=tables_response_,
        )
    )
    layout = DepsParser(unified_data_image_page1, ParsingType.TESSERACT).add_response_to_page(response, document_layout)

    assert len(layout.pages) == 1
    assert len(layout.pages[0].tables) == 1
    assert len(layout.pages[0].paragraphs) == 1
    assert layout.pages[0].id() == unified_data_image_page1.id
    assert layout.pages[0].dimension.width == unified_data_image_page1.width
    assert layout.pages[0].dimension.height == unified_data_image_page1.height
    assert layout.pages[0].dimension.unit == "px"
    assert (
        layout.pages[0].transformations.angle
        == unified_data_image_page1.applied_transformation.parameters.kwargs["angle"]
    )
    assert (
        layout.pages[0].transformations.orientation
        == unified_data_image_page1.applied_transformation.parameters.kwargs["orientation"]
    )


def test_deps_parser__no_data__no_errors(unified_data_image_page1, document_layout):
    response = DepsStructuredResponse(dict(ocr_data=None, tables_data=None))
    layout = DepsParser(unified_data_image_page1, ParsingType.TESSERACT).add_response_to_page(response, document_layout)

    assert len(layout.pages) == 1
    assert len(layout.pages[0].tables) == 0
    assert len(layout.pages[0].paragraphs) == 0
    assert layout.pages[0].id() == unified_data_image_page1.id
    assert layout.pages[0].dimension.width == unified_data_image_page1.width
    assert layout.pages[0].dimension.height == unified_data_image_page1.height
    assert layout.pages[0].dimension.unit == "px"
    assert (
        layout.pages[0].transformations.angle
        == unified_data_image_page1.applied_transformation.parameters.kwargs["angle"]
    )
    assert (
        layout.pages[0].transformations.orientation
        == unified_data_image_page1.applied_transformation.parameters.kwargs["orientation"]
    )
