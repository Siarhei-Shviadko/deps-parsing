from sqlalchemy import Column, Index, Integer, String, Table
from sqlalchemy.dialects.postgresql import JSONB

from deps_parsing.extras.datasource import metadata

__all__ = ["cell_table"]


cell_table = Table(
    "tabular_layout__cell",
    metadata,
    Column("id", String, primary_key=True),
    Column("tabular_layout_id", String),
    Column("table_id", String),
    Column("content", String),
    Column("data_type", String),
    Column("relative_position_row", Integer),
    Column("relative_position_column", Integer),
    Column("absolute_position_row", Integer),
    Column("absolute_position_column", Integer),
    Column("merge", JSONB),
    Column("style", JSONB),
    Column("comment", JSONB),
    Column("alignment", JSONB),
    Column("borders", JSONB),
    Index(
        "idx_tl_table_cell_position",
        "tabular_layout_id",
        "table_id",
        "relative_position_row",
        "relative_position_column",
    ),
)
