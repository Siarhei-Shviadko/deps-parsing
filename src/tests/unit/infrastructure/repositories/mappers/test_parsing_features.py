from deps_document_layout.model import ParsingFeature, ParsingType

from deps_parsing.infrastructure.repositories.document_layout.mappers import (
    ParsingFeaturesMapper,
)


def test_parsing_features_mapper():
    parsing_features = {
        ParsingType.AZURE_FORM_RECOGNIZER: {ParsingFeature.IMAGES, ParsingFeature.TABLES},
        ParsingType.AWS_TEXTRACT: {ParsingFeature.TEXT, ParsingFeature.KEY_VALUE_PAIRS},
    }

    res = ParsingFeaturesMapper.from_dict(ParsingFeaturesMapper.to_dict(parsing_features))

    assert res == parsing_features
