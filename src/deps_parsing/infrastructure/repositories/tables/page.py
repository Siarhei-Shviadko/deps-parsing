from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    PrimaryKeyConstraint,
    String,
    Table,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB

from deps_parsing.extras.datasource import metadata

__all__ = ["page_table"]

page_table = Table(
    "page",
    metadata,
    Column("id", String, primary_key=True),
    Column("page_number", Integer, nullable=False),
    Column("parsing_type", String, primary_key=True),
    Column("dimension", JSONB, nullable=False),
    Column("languages", JSONB, nullable=False),
    Column("file_path", String, nullable=False),
    Column("transformations", JSONB, nullable=False),
    Column("groups", JSONB, nullable=False),
    Column(
        "document_layout_id",
        String,
        ForeignKey("document_layout.id", ondelete="cascade", name="document_layout_id_fkey"),
    ),
    UniqueConstraint(
        "document_layout_id",
        "page_number",
        "parsing_type",
        name="unique__document_layout_id__page_number__parsing_type",
    ),
    PrimaryKeyConstraint(name="page_id_parsing_type_pk"),
)
