import factory
from deps_document_layout.model import EntityId, KeyValuePair, KeyValuePairElement
from faker import Faker

from .base_line_element import PolygonFactory

__all__ = ["KeyValuePairElementFactory", "KeyValuePairFactory"]

fake = Faker()


class KeyValuePairElementFactory(factory.Factory):
    class Meta:
        model = KeyValuePairElement

    paragraph_id = factory.LazyAttribute(lambda _: EntityId(fake.pystr()))
    content = fake.name()
    polygon = factory.SubFactory(PolygonFactory)


class KeyValuePairFactory(factory.Factory):
    class Meta:
        model = KeyValuePair

    id_ = factory.LazyAttribute(lambda _: EntityId(fake.pystr()))
    order = factory.Sequence(lambda n: n + 1)
    confidence = fake.pyfloat(min_value=0, max_value=1)
    key = factory.SubFactory(KeyValuePairElementFactory)
    value = factory.LazyFunction(lambda: KeyValuePairElementFactory() if fake.boolean() else None)
