import uuid

import factory
import factory.fuzzy as fuzzy
from deps_document_layout.model import EntityId, TenantId
from faker import Faker

from deps_parsing.domain.model import CommandChannel, DocumentType

__all__ = ["DocumentTypeFactory"]

fake = Faker()


class DocumentTypeFactory(factory.Factory):
    class Meta:
        model = DocumentType

    id_ = factory.LazyFunction(lambda: EntityId(uuid.uuid4().hex))
    tenant_id = factory.LazyFunction(lambda: TenantId(uuid.uuid4().hex))
    command_channel = fuzzy.FuzzyChoice([None, CommandChannel(fake.name())])
