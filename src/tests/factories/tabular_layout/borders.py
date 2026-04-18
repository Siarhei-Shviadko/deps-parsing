import factory
from deps_tabular_layout.models import Borders

__all__ = ["BordersFactory"]


class BordersFactory(factory.Factory):
    class Meta:
        model = Borders

    top = factory.Faker("word")
    bottom = factory.Faker("word")
    left = factory.Faker("word")
    right = factory.Faker("word")
