from sqlalchemy import Column, String, Table, UniqueConstraint

from deps_parsing.extras.datasource import metadata

__all__ = ["document_type_table"]

VARCHAR_LENGTH = 150

document_type_table = Table(
    "document_type",
    metadata,
    Column("id", String(VARCHAR_LENGTH), primary_key=True),
    Column("tenant_id", String(VARCHAR_LENGTH), nullable=False),
    Column("command_channel", String(VARCHAR_LENGTH)),
    UniqueConstraint("id", "tenant_id", name="unique__document_type_id__tenant_id"),
)
