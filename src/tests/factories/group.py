import factory
from deps_document_layout.model import EntityId, Group
from faker import Faker

__all__ = ["GroupFactory"]

fake = Faker()


class GroupFactory(factory.Factory):
    class Meta:
        model = Group

    id_ = factory.LazyFunction(lambda: EntityId(fake.uuid4()))
    name = factory.Faker("pystr")
    members = factory.LazyFunction(
        lambda: frozenset(EntityId(fake.uuid4()) for _ in range(fake.pyint(min_value=1, max_value=10)))
    )
