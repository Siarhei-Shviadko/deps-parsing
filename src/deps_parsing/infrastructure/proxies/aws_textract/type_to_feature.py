from types import MappingProxyType

from deps_document_layout.model import ParsingFeature

from .aws_features import AWSFeature

PARSING_TYPE_TO_AWS_FEATURE_MAPPING = MappingProxyType(
    {
        ParsingFeature.KEY_VALUE_PAIRS: AWSFeature.FORMS,
        ParsingFeature.TABLES: AWSFeature.TABLES,
        ParsingFeature.IMAGES: AWSFeature.LAYOUT,
        ParsingFeature.TEXT: None,  # extracted with any parameters
    },
)
