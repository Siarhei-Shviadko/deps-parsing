from sqlalchemy import Column, String, Table, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB

from deps_parsing.extras.datasource import metadata

__all__ = ["document_layout_table"]

document_layout_table = Table(
    "document_layout",
    metadata,
    Column("id", String, primary_key=True, nullable=False),
    Column("tenant_id", String, primary_key=True, nullable=False),
    Column("parsing_features", JSONB, nullable=False),
    Column("merged_tables", JSONB),
    UniqueConstraint(
        "id",
        "tenant_id",
        name="document_layout_id__tenant_id__pk",
    ),
)
