from typing import Optional

from sqlalchemy import and_, delete, select
from sqlalchemy.dialects.postgresql import insert as pg_insert

from deps_parsing.domain.model import DocumentType, IDocumentTypeRepository
from deps_parsing.extras.datasource import Database

from ..tables import document_type_table
from .mapper import DocumentTypeMapper

__all__ = ["DocumentTypeRepository"]


class DocumentTypeRepository(IDocumentTypeRepository):
    def __init__(self, database: Database) -> None:
        self._db = database
        self._schema = document_type_table

    def find_by_id_for_tenant(self, document_type_id: str, tenant_id: str) -> Optional[DocumentType]:
        query = select([self._schema]).where(
            and_(self._schema.c.id == document_type_id, self._schema.c.tenant_id == tenant_id),
        )

        with self._db.connection() as conn:
            if rows := conn.execute(query).fetchone():
                return DocumentTypeMapper.from_dict(rows)

    def find_by_id(self, document_type_id: str) -> Optional[DocumentType]:
        query = select([self._schema]).where(self._schema.c.id == document_type_id)
        with self._db.connection() as conn:
            if row := conn.execute(query).fetchone():
                return DocumentTypeMapper.from_dict(row)

    def save(self, document_type: DocumentType) -> None:
        raw_document_layout = DocumentTypeMapper.to_dict(document_type)
        with self._db.connection() as conn:
            query = pg_insert(self._schema).values(**raw_document_layout)
            query = query.on_conflict_do_update(constraint=self._schema.primary_key, set_=dict(query.excluded))
            conn.execute(query)

    def save_all(self, document_types: list[DocumentType]) -> None:
        if document_types:
            raw_doc_types = [DocumentTypeMapper.to_dict(doc_type) for doc_type in document_types]
            with self._db.connection() as conn:
                query = pg_insert(document_type_table)
                query = query.on_conflict_do_update(constraint=self._schema.primary_key, set_=dict(query.excluded))
                conn.execute(query, raw_doc_types)

    def delete(self, document_type_id: str) -> None:
        with self._db.connection() as conn:
            query = delete(self._schema).where(self._schema.c.id == document_type_id)
            conn.execute(query)
