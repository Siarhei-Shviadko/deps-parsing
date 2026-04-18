from abc import ABC, abstractmethod

from .document_type import DocumentType

__all__ = ["IDocumentTypeRepository"]


class IDocumentTypeRepository(ABC):
    @abstractmethod
    def find_by_id_for_tenant(self, document_type_id: str, tenant_id: str) -> DocumentType:
        pass

    @abstractmethod
    def save(self, document_type: DocumentType) -> None:
        pass

    @abstractmethod
    def save_all(self, document_types: list[DocumentType]) -> None:
        pass

    @abstractmethod
    def find_by_id(self, document_type_id: str) -> DocumentType:
        pass

    @abstractmethod
    def delete(self, document_type_id: str) -> None:
        pass
