from sqlalchemy import Column, Integer, String, Table
from sqlalchemy.dialects.postgresql import JSONB

from deps_parsing.extras.datasource import metadata

__all__ = ["tbl_table"]


tbl_table = Table(
    "tabular_layout__table",
    metadata,
    Column("id", String, primary_key=True),
    Column("tabular_layout_id", String),
    Column("sheet_id", String),
    Column("column_count", Integer),
    Column("row_count", Integer),
    Column("placement", JSONB),
)
