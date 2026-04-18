from uuid import uuid4

import factory
from deps_tabular_layout.models import EntityId, Sheet

from .image import ImageFactory
from .table import TableFactory

__all__ = ["SheetFactory"]


class SheetFactory(factory.Factory):
    class Meta:
        model = Sheet

    id_ = factory.LazyFunction(lambda: EntityId(uuid4().hex))
    title = factory.Faker("sentence", nb_words=4)
    is_hidden = factory.Faker("boolean")
    tables = factory.List([factory.SubFactory(TableFactory) for _ in range(2)])
    images = factory.List([factory.SubFactory(ImageFactory) for _ in range(3)])
