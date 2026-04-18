from uuid import uuid4

import factory
from deps_tabular_layout.models import EntityId, Image, ImageType

from .point import PointFactory

__all__ = ["ImageFactory"]


class ImageFactory(factory.Factory):
    class Meta:
        model = Image

    id_ = factory.LazyFunction(lambda: EntityId(uuid4().hex))
    file_path = factory.Faker("file_path")
    type_ = factory.Iterator([ImageType.PICTURE, ImageType.CHART])
    position = factory.SubFactory(PointFactory)
    title = factory.Faker("sentence")
    description = factory.Faker("paragraph")
