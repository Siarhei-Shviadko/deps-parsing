import factory
from deps_document_layout.model import Dimension, Language
from faker import Faker

__all__ = ["DimensionFactory", "LanguageFactory"]

fake = Faker()


class DimensionFactory(factory.Factory):
    class Meta:
        model = Dimension

    width = fake.pyint(min_value=1)
    height = fake.pyint(min_value=1)
    unit = fake.pystr()


class LanguageFactory(factory.Factory):
    class Meta:
        model = Language

    language_code = fake.language_code()
    confidence = fake.pyfloat(min_value=0, max_value=1)
