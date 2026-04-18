import factory
import factory.fuzzy as fuzzy
from deps_document_layout.model import EntityId, Page, ParsingType
from faker import Faker

from .image import ImageFactory
from .key_value_pair import KeyValuePairFactory
from .page_elements import DimensionFactory, LanguageFactory
from .paragraph import ParagraphFactory
from .table import TableFactory
from .transformation import TransformationsFactory

__all__ = ["PageFactory"]

fake = Faker()


class PageFactory(factory.Factory):
    class Meta:
        model = Page

    id_ = factory.LazyAttribute(lambda _: EntityId(fake.pystr()))
    page_number = factory.Sequence(lambda n: n + 1)
    parsing_type = fuzzy.FuzzyChoice(list(ParsingType))
    dimension = factory.SubFactory(DimensionFactory)
    languages = factory.LazyFunction(lambda: tuple(LanguageFactory() for _ in range(fake.pyint(max_value=4))))
    file_path = fake.file_path()
    transformations = factory.SubFactory(TransformationsFactory)

    images = factory.LazyFunction(lambda: tuple(ImageFactory() for _ in range(fake.pyint(max_value=5))))
    key_value_pairs = factory.LazyFunction(lambda: tuple(KeyValuePairFactory() for _ in range(fake.pyint(max_value=5))))
    paragraphs = factory.LazyFunction(lambda: tuple(ParagraphFactory() for _ in range(fake.pyint(max_value=5))))
    tables = factory.LazyFunction(lambda: tuple(TableFactory() for _ in range(fake.pyint(max_value=5))))
