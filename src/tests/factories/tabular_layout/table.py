from uuid import uuid4

import factory
from deps_tabular_layout.models import EntityId, Table

from .point import PointFactory

__all__ = ["TableFactory"]


class TableFactory(factory.Factory):
    class Meta:
        model = Table

    id_ = factory.LazyFunction(lambda: EntityId(uuid4().hex))
    sheet_id = factory.LazyFunction(lambda: EntityId(uuid4().hex))
    column_count = factory.Faker("random_int", min=1, max=10)
    row_count = factory.Faker("random_int", min=1, max=10)
    placement = factory.LazyAttribute(lambda o: (PointFactory(), PointFactory()))
