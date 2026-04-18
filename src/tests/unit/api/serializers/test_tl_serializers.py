from deps_parsing.api.serializers import (
    SerializedSheet,
    SerializedTable,
    SerializedTabularLayout,
)
from tests.data.tabular_layout import tabular_layout_projection


def test_tl_serializer__ok():
    serialized_proj = SerializedTabularLayout.from_model(tabular_layout_projection)

    assert serialized_proj.id == tabular_layout_projection.id
    assert serialized_proj.tenant_id == tabular_layout_projection.tenant_id
    assert serialized_proj.extracted_properties == list(tabular_layout_projection.extracted_properties)
    assert serialized_proj.parsing_type == tabular_layout_projection.parsing_type
    assert serialized_proj.tables
    assert serialized_proj.sheets


def test_sheet_serializer__ok():
    orig_sheet = tabular_layout_projection.sheets[0]
    serialized_proj = SerializedSheet.from_model(orig_sheet)

    assert serialized_proj.id == orig_sheet.id
    assert serialized_proj.title == orig_sheet.title
    assert serialized_proj.is_hidden == orig_sheet.is_hidden
    assert serialized_proj.table_ids == [table_id for table_id in orig_sheet.table_ids]
    assert serialized_proj.images
    assert serialized_proj.tables is None


def test_table_serializer__ok():
    orig_table = tabular_layout_projection.tables[0]

    serialized_proj = SerializedTable.from_model(orig_table)

    assert len(serialized_proj.data) == len(orig_table.data)
    assert serialized_proj.schema_.id == orig_table.schema.id
    assert serialized_proj.schema_.sheet_id == orig_table.schema.sheet_id
    assert serialized_proj.schema_.column_count == orig_table.schema.column_count
    assert serialized_proj.schema_.row_count == orig_table.schema.row_count
    assert list(serialized_proj.schema_.placement[0].values()) == [
        orig_table.schema.placement[0].x,
        orig_table.schema.placement[0].y,
    ]
    assert list(serialized_proj.schema_.placement[1].values()) == [
        orig_table.schema.placement[1].x,
        orig_table.schema.placement[1].y,
    ]
