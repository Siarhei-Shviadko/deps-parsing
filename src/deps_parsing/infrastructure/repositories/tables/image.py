from sqlalchemy import (
    Column,
    ForeignKeyConstraint,
    Integer,
    PrimaryKeyConstraint,
    String,
    Table,
    Text,
)
from sqlalchemy.dialects.postgresql import JSONB

from deps_parsing.extras.datasource import metadata

__all__ = ["image_table"]

image_table = Table(
    "image",
    metadata,
    Column("id", String, primary_key=True),
    Column("order_num", Integer, nullable=False),
    Column("title", String),
    Column("file_path", String, nullable=False),
    Column("polygon", JSONB, nullable=False),
    Column("description", Text),
    Column("page_id", String, nullable=False),
    Column("parsing_type", String(100), nullable=False),
    ForeignKeyConstraint(
        columns=("page_id", "parsing_type"),
        refcolumns=("page.id", "page.parsing_type"),
        name="image_page_fk",
        ondelete="CASCADE",
    ),
    PrimaryKeyConstraint("id", name="image_pk"),
)
