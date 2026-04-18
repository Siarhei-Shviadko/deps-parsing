from uuid import uuid4

from deps_tabular_layout.models import (
    CellProperties,
    EntityId,
    Image,
    ImageType,
    ParsingType,
    Point,
    Sheet,
    Table,
    TabularLayout,
    TenantId,
)

from deps_parsing.domain.dtos import (
    SheetProjection,
    TableProjection,
    TableSchemaProjection,
    TabularLayoutProjection,
)

from ..factories.tabular_layout import CellFactory

__all__ = ["tabular_layout"]

document_id = uuid4().hex
tenant_id = uuid4().hex
sheet_1_id = uuid4().hex
sheet_2_id = uuid4().hex
table_1_id = uuid4().hex
table_2_id = uuid4().hex

table_1_placement = (
    Point(
        x=1,
        y=1,
    ),
    Point(x=10, y=10),
)
table_2_placement = (
    Point(
        x=1,
        y=1,
    ),
    Point(x=5, y=5),
)
table_for_sheet_1 = Table(
    id_=EntityId(uuid4().hex),
    sheet_id=EntityId(sheet_1_id),
    column_count=10,
    row_count=10,
    placement=table_1_placement,
)
table_for_sheet_2 = Table(
    id_=EntityId(uuid4().hex),
    sheet_id=EntityId(sheet_2_id),
    column_count=5,
    row_count=5,
    placement=table_2_placement,
)
image_for_sheet_1 = Image(
    id_=EntityId(uuid4().hex),
    file_path=uuid4().hex,
    type_=ImageType.PICTURE,
    position=None,
    title=uuid4().hex,
    description=uuid4().hex,
)

image_for_sheet_2 = Image(
    id_=EntityId(uuid4().hex),
    file_path=uuid4().hex,
    type_=ImageType.CHART,
    position=Point(x=15, y=15),
    title=uuid4().hex,
    description=uuid4().hex,
)
sheet_1 = Sheet(
    id_=EntityId(sheet_1_id),
    title=uuid4().hex,
    is_hidden=False,
    tables=[table_for_sheet_1],
    images=[image_for_sheet_1],
)

sheet_2 = Sheet(
    id_=EntityId(sheet_2_id),
    title=uuid4().hex,
    is_hidden=False,
    tables=[table_for_sheet_2],
    images=[image_for_sheet_2],
)

tabular_layout = TabularLayout(
    id_=EntityId(document_id),
    tenant_id=TenantId(tenant_id),
    parsing_type=ParsingType.CSV,
    sheets=[sheet_1, sheet_2],
    extracted_properties=[
        CellProperties.ALIGNMENT,
        CellProperties.BORDERS,
        CellProperties.COMMENTS,
        CellProperties.STYLING,
    ],
)

table_projection_for_sheet_1 = TableProjection(
    schema=TableSchemaProjection(
        id=table_1_id,
        sheet_id=sheet_1_id,
        column_count=10,
        row_count=10,
        placement=table_1_placement,
    ),
    data=[CellFactory(table_id=EntityId(table_1_id)) for _ in range(5)],
)

table_projection_for_sheet_2 = TableProjection(
    schema=TableSchemaProjection(
        id=uuid4().hex,
        sheet_id=sheet_2_id,
        column_count=10,
        row_count=10,
        placement=table_2_placement,
    ),
    data=[CellFactory(table_id=EntityId(table_1_id)) for _ in range(5)],
)

sheet_1_projection = SheetProjection(
    id=sheet_1_id,
    title=uuid4().hex,
    is_hidden=False,
    table_ids=[table_for_sheet_1.id()],
    images=[image_for_sheet_1],
)

sheet_2_projection = SheetProjection(
    id=sheet_2_id,
    title=uuid4().hex,
    is_hidden=False,
    table_ids=[table_for_sheet_2.id()],
    images=[image_for_sheet_2],
)

tabular_layout_projection = TabularLayoutProjection(
    id=document_id,
    tenant_id=tenant_id,
    parsing_type=ParsingType.CSV,
    extracted_properties=[
        CellProperties.ALIGNMENT,
        CellProperties.BORDERS,
        CellProperties.COMMENTS,
        CellProperties.STYLING,
    ],
    sheets=[sheet_1_projection, sheet_2_projection],
    tables=[table_projection_for_sheet_1, table_projection_for_sheet_2],
)
