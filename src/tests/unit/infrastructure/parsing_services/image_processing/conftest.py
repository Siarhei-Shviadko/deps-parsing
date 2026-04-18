import pytest


@pytest.fixture
def test_page_image() -> bytes:
    with open("tests/data/image_processing/faces-processed-image.png", "rb") as file:
        return file.read()


@pytest.fixture
def expected_cropped_image() -> bytes:
    with open("tests/data/image_processing/expected-cropped.png", "rb") as file:
        return file.read()


@pytest.fixture
def test_small_image() -> bytes:
    with open("tests/data/image_processing/small-image.png", "rb") as file:
        return file.read()
