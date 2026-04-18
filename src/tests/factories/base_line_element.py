import factory
from deps_document_layout.model import BaseLineElement
from faker import Faker

from .polygon import PolygonFactory

__all__ = ["BaseLineElementFactory"]

fake = Faker()


class BaseLineElementFactory(factory.Factory):
    class Meta:
        model = BaseLineElement

    order = factory.Sequence(lambda n: n + 1)
    confidence = fake.pyfloat(min_value=0, max_value=1)
    polygon = factory.SubFactory(PolygonFactory)
