from io import BytesIO
from typing import Optional

from deps_document_layout.model import DocumentLayout, ParsingFeature, ParsingType
from deps_object_storage import ObjectStorage
from docx import Document as DocxDocument

from ...docx import DOCXParser
from ..abstract_service import IParseDocuments

__all__ = ["DOCXParsingService"]


class DOCXParsingService(IParseDocuments):
    parsing_type: ParsingType = ParsingType.DOCX
    processable_features = {ParsingFeature.TEXT, ParsingFeature.TABLES}

    def __init__(self, storage: ObjectStorage) -> None:
        super().__init__()
        self._storage = storage

    def parse(
        self,
        file_path: str,
        document_layout: DocumentLayout,
        features: set[ParsingFeature],
        language: Optional[str] = None,
    ) -> tuple[DocumentLayout, None]:
        self._logger.info(
            "Document analyzing for document layout %s with features %s has been started",
            document_layout.id(),
            [feature.value for feature in features],
        )
        blob_content: bytes = self._storage.download(file_path)

        with BytesIO(blob_content) as docx_file:
            docx_document = DocxDocument(docx_file)

        self.add_page_to_document_layout(document_layout, docx_document)
        document_layout.update_parsing_features(self.parsing_type, features)

        return document_layout, None

    def add_page_to_document_layout(self, document_layout: DocumentLayout, docx_document: DocxDocument) -> None:
        DOCXParser(docx_document).add_page_to(document_layout)
