import pytest
from deps_document_layout.model import (
    DocumentLayoutFeaturesFilter,
    ParsingFeature,
    ParsingType,
)


@pytest.fixture
def test_features_filter():
    return DocumentLayoutFeaturesFilter(
        parsing_type=ParsingType.AWS_TEXTRACT,
        features={ParsingFeature.TEXT, ParsingFeature.TABLES, ParsingFeature.IMAGES, ParsingFeature.KEY_VALUE_PAIRS},
    )


@pytest.fixture
def save_document_layout(document_layout_repository, document_layout) -> None:
    document_layout_repository.save(document_layout)
