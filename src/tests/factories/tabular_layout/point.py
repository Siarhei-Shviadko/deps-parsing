import random

import factory
from deps_tabular_layout.models import Point
from pytest_factoryboy import register

__all__ = ["PointFactory"]


@register
class PointFactory(factory.Factory):
    class Meta:
        model = Point

    x = factory.LazyFunction(lambda: random.randint(0, 100))
    y = factory.LazyFunction(lambda: random.randint(0, 100))
