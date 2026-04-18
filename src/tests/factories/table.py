import factory
from deps_document_layout.model import Cell, EntityId, Table
from faker import Faker

from .polygon import PolygonFactory

__all__ = ["CellFactory", "TableFactory"]

fake = Faker()


class CellFactory(factory.Factory):
    class Meta:
        model = Cell

    paragraph_id = factory.LazyAttribute(lambda _: EntityId(fake.pystr()))
    content = fake.pystr()
    column_index = fake.pyint(min_value=0, max_value=100)
    column_span = fake.pyint(min_value=1, max_value=10)
    row_index = fake.pyint(min_value=0, max_value=100)
    row_span = fake.pyint(min_value=1, max_value=10)
    polygon = factory.SubFactory(PolygonFactory)
    kind = fake.pystr()


class TableFactory(factory.Factory):
    class Meta:
        model = Table

    id_ = factory.LazyAttribute(lambda _: EntityId(fake.pystr()))
    order = factory.Sequence(lambda n: n + 1)
    cells = factory.LazyFunction(lambda: tuple(CellFactory() for _ in range(fake.pyint(max_value=10))))
    confidence = fake.pyfloat(min_value=0, max_value=1)
    column_count = fake.pyint(min_value=1, max_value=50)
    row_count = fake.pyint(min_value=1, max_value=50)
    polygon = factory.SubFactory(PolygonFactory)
