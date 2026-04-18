import random

import factory
from deps_tabular_layout.models import Alignment

__all__ = ["AlignmentFactory"]


class AlignmentFactory(factory.Factory):
    class Meta:
        model = Alignment

    horizontal = factory.Faker("word")
    vertical = factory.Faker("word")
    rotation = random.randint(1, 10)
