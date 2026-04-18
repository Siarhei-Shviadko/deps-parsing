from .abstract_service import *
from .aws_textract import (
    AWSTextractDocumentParsingService as AWSTextractDocumentParsingServiceV2,
)
from .aws_textract import (
    AWSTextractPageParsingService as AWSTextractPageParsingServiceV2,
)
from .azure import AzureDocumentParsingService as AzureDocumentParsingServiceV2
from .azure import AzurePageParsingService as AzurePageParsingServiceV2
from .deps import TesseractParsingService as TesseractParsingServiceV2
from .document_based_service import *
from .docx import DOCXParsingService as DOCXParsingServiceV2
from .google import (
    DocumentAIDocumentParsingService as DocumentAIDocumentParsingServiceV2,
)
from .google import DocumentAIPageParsingService as DocumentAIPageParsingServiceV2
from .page_based_service import *

__all__ = (
    [
        TesseractParsingServiceV2,
        DocumentAIPageParsingServiceV2,
        DocumentAIDocumentParsingServiceV2,
        AWSTextractDocumentParsingServiceV2,
        AWSTextractPageParsingServiceV2,
        AzureDocumentParsingServiceV2,
        AzurePageParsingServiceV2,
        DOCXParsingServiceV2,
    ]
    + abstract_service.__all__
    + page_based_service.__all__
    + document_based_service.__all__
)
