from sqlalchemy import (
    Column,
    Float,
    ForeignKeyConstraint,
    Integer,
    PrimaryKeyConstraint,
    String,
    Table,
    Text,
)
from sqlalchemy.dialects.postgresql import JSONB

from deps_parsing.extras.datasource import metadata

__all__ = ["paragraph_table"]

paragraph_table = Table(
    "paragraph",
    metadata,
    Column("id", String, primary_key=True),
    Column("order_num", Integer, nullable=False),
    Column("content", Text, nullable=False),
    Column("confidence", Float),
    Column("role", String),
    Column("polygon", JSONB, nullable=False),
    Column("lines", JSONB, nullable=False),
    Column("page_id", String, nullable=False),
    Column("parsing_type", String, nullable=False),
    ForeignKeyConstraint(
        columns=("page_id", "parsing_type"),
        refcolumns=("page.id", "page.parsing_type"),
        name="paragraph_page_fk",
        ondelete="CASCADE",
    ),
    PrimaryKeyConstraint(name="paragraph_pk"),
)
