import factory
from deps_document_layout.model import EntityId, Image
from faker import Faker

from .polygon import PolygonFactory

__all__ = ["ImageFactory"]

fake = Faker()


class ImageFactory(factory.Factory):
    class Meta:
        model = Image

    id_ = factory.LazyAttribute(lambda _: EntityId(fake.pystr()))
    order = factory.Sequence(lambda n: n + 1)
    title = fake.company()
    file_path = fake.file_path()
    polygon = factory.SubFactory(PolygonFactory)
