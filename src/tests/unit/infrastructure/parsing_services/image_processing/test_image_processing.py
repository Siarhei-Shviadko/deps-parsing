import platform
from unittest.mock import MagicMock

import pytest
from deps_document_layout.model import Point

from deps_parsing.infrastructure.dl_parsing.image_processing import (
    OCRLayoutImageProcessingService,
    PreparsedImage,
)


@pytest.mark.skipif(platform.system() == "Darwin", reason="Skip on macOS")
def test_image_cropping__with__annotations(
    storage_mock: MagicMock,
    ai_fusion_mock: MagicMock,
    ocr_image_processing_service: OCRLayoutImageProcessingService,
    test_page_image: bytes,
    expected_cropped_image: bytes,
) -> None:
    test_title, test_description = "some-title", "some-description"
    polygon = tuple(
        [
            Point(0.03442889824509621, 0.48392993211746216),
            Point(0.3012491762638092, 0.48107674717903137),
            Point(0.305982768535614, 0.8419623970985413),
            Point(0.03878959268331528, 0.8438605070114136),
        ],
    )
    ai_fusion_mock.retrieve_image_insights.return_value = {
        "title": {"content": test_title, "errorOccurred": False},
        "description": {"content": test_description, "errorOccurred": False},
    }

    cropped = ocr_image_processing_service.process_preparsed_image(
        preparsed_image=PreparsedImage(
            layout_id="test_layout_id",
            page_image=test_page_image,
            polygon=polygon,
        ),
    )

    storage_mock.upload.assert_called_once_with(
        path=cropped.filepath,
        content=expected_cropped_image,
        replace_if_exists=True,
    )

    assert cropped.title == test_title
    assert cropped.description == test_description


@pytest.mark.skipif(platform.system() == "Darwin", reason="Skip on macOS")
def test_image_cropping__with__annotations_error(
    storage_mock: MagicMock,
    ai_fusion_mock: MagicMock,
    ocr_image_processing_service: OCRLayoutImageProcessingService,
    test_page_image: bytes,
    expected_cropped_image: bytes,
) -> None:
    test_description = "test_description"
    polygon = tuple(
        [
            Point(0.03442889824509621, 0.48392993211746216),
            Point(0.3012491762638092, 0.48107674717903137),
            Point(0.305982768535614, 0.8419623970985413),
            Point(0.03878959268331528, 0.8438605070114136),
        ],
    )
    ai_fusion_mock.retrieve_image_insights.return_value = {
        "title": {"content": "test_title", "errorOccurred": True},
        "description": {"content": test_description, "errorOccurred": True},
    }

    cropped = ocr_image_processing_service.process_preparsed_image(
        preparsed_image=PreparsedImage(
            layout_id="test_layout_id",
            page_image=test_page_image,
            polygon=polygon,
        ),
    )

    storage_mock.upload.assert_called_once_with(
        path=cropped.filepath,
        content=expected_cropped_image,
        replace_if_exists=True,
    )

    assert cropped.title == "Annotation error occurred"
    assert cropped.description == f"Error occurred: {test_description}"


@pytest.mark.skipif(platform.system() == "Darwin", reason="Skip on macOS")
def test_image_cropping__small_image__skip_annotation(
    storage_mock: MagicMock,
    ai_fusion_mock: MagicMock,
    ocr_image_processing_service: OCRLayoutImageProcessingService,
    test_small_image: bytes,
) -> None:
    polygon = tuple(
        [
            Point(0.0, 0.0),
            Point(1.0, 0.0),
            Point(1.0, 1.0),
            Point(0.0, 1.0),
        ],
    )
    ai_fusion_mock.retrieve_image_insights.return_value = {
        "title": {"content": "test_title", "errorOccurred": True},
        "description": {"content": "test_description", "errorOccurred": True},
    }

    cropped = ocr_image_processing_service.process_preparsed_image(
        preparsed_image=PreparsedImage(
            layout_id="test_layout_id",
            page_image=test_small_image,
            polygon=polygon,
        ),
    )

    storage_mock.upload.assert_called_once_with(
        path=cropped.filepath,
        content=test_small_image,
        replace_if_exists=True,
    )
    ai_fusion_mock.retrieve_image_insights.assert_not_called()
