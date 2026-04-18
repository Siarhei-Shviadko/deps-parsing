import factory
from deps_document_layout.model import EntityId, Paragraph
from faker import Faker

from .line import LineFactory
from .polygon import PolygonFactory

__all__ = ["ParagraphFactory"]

fake = Faker()


class ParagraphFactory(factory.Factory):
    class Meta:
        model = Paragraph

    id_ = factory.LazyAttribute(lambda _: EntityId(fake.pystr()))
    order = factory.Sequence(lambda n: n + 1)
    confidence = fake.pyfloat(min_value=0, max_value=1)
    content = fake.name()
    role = fake.pystr(min_chars=3, max_chars=10, prefix="ROLE_")
    polygon = factory.SubFactory(PolygonFactory)
    lines = factory.LazyFunction(lambda: tuple(LineFactory() for _ in range(fake.pyint(min_value=1, max_value=10))))
