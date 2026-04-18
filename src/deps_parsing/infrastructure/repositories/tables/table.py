from sqlalchemy import (
    Column,
    Float,
    ForeignKeyConstraint,
    Integer,
    PrimaryKeyConstraint,
    String,
    Table,
)
from sqlalchemy.dialects.postgresql import JSONB

from deps_parsing.extras.datasource import metadata

__all__ = ["table_table"]

table_table = Table(
    "table_",
    metadata,
    Column("id", String, primary_key=True),
    Column("order_num", Integer, nullable=False),
    Column("column_count", Integer, nullable=False),
    Column("row_count", Integer, nullable=False),
    Column("polygon", JSONB, nullable=False),
    Column("confidence", Float),
    Column("cells", JSONB, nullable=False),
    Column("page_id", String, nullable=False),
    Column("parsing_type", String, nullable=False),
    ForeignKeyConstraint(
        columns=("page_id", "parsing_type"),
        refcolumns=("page.id", "page.parsing_type"),
        name="table_page_fk",
        ondelete="CASCADE",
    ),
    PrimaryKeyConstraint(name="table_pk"),
)
