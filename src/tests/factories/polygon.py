import random

import factory
from deps_document_layout.model import Point
from faker import Faker

__all__ = ["PolygonFactory"]

fake = Faker()


class PointFactory(factory.Factory):
    class Meta:
        model = Point

    x = factory.LazyFunction(lambda: fake.pyfloat(min_value=0, max_value=1))
    y = factory.LazyFunction(lambda: fake.pyfloat(min_value=0, max_value=1))


class PolygonFactory(factory.Factory):
    class Meta:
        model = tuple
        inline_args = ("polygon",)

    polygon = factory.LazyFunction(lambda: tuple(PointFactory() for _ in range(random.randint(4, 10))))
