from sqlalchemy import Column, String, Table
from sqlalchemy.dialects.postgresql import JSONB

from deps_parsing.extras.datasource import metadata

__all__ = ["tabular_layout_table"]


tabular_layout_table = Table(
    "tabular_layout",
    metadata,
    Column("id", String, primary_key=True),
    Column("tenant_id", String, primary_key=True),
    Column("parsing_type", String, nullable=False),
    Column("sheets", JSONB),
    Column("extracted_properties", JSONB),
)
