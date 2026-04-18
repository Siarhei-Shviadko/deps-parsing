import random
from uuid import uuid4

import factory
from deps_tabular_layout.models import (
    CellProperties,
    EntityId,
    ParsingType,
    TabularLayout,
    TenantId,
)

from .sheet import SheetFactory

__all__ = ["TabularLayoutFactory"]


class TabularLayoutFactory(factory.Factory):
    class Meta:
        model = TabularLayout

    id_ = factory.LazyFunction(lambda: EntityId(uuid4().hex))
    tenant_id = factory.LazyFunction(lambda: TenantId(uuid4().hex))
    parsing_type = factory.Iterator([ParsingType.CSV, ParsingType.EXCEL])
    sheets = factory.List([factory.SubFactory(SheetFactory) for _ in range(3)])
    extracted_properties = random.sample(
        [CellProperties.ALIGNMENT, CellProperties.BORDERS, CellProperties.COMMENTS, CellProperties.STYLING],
        k=random.randint(1, 4),
    )
