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

__all__ = ["key_value_pair_table"]

key_value_pair_table = Table(
    "key_value_pair",
    metadata,
    Column("id", String, primary_key=True),
    Column("order_num", Integer, nullable=False),
    Column("key", JSONB, nullable=False),
    Column("value", JSONB),
    Column("confidence", Float, nullable=False),
    Column("page_id", String, nullable=False),
    Column("parsing_type", String, nullable=False),
    ForeignKeyConstraint(
        columns=("page_id", "parsing_type"),
        refcolumns=("page.id", "page.parsing_type"),
        name="key_value_pair_page_fk",
        ondelete="CASCADE",
    ),
    PrimaryKeyConstraint(name="key_value_pair_pk"),
)
