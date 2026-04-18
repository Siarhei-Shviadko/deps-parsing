import factory
from deps_document_layout.model import Barcode, Formula, SelectionMark, Signature, Word
from faker import Faker

from .base_line_element import BaseLineElementFactory
from .style import StyleFactory

__all__ = [
    "WordFactory",
    "SigntureFactory",
    "SelectionMarkFactory",
    "FormulaFactory",
    "BarcodeFactory",
]

fake = Faker()


class WordFactory(BaseLineElementFactory):
    class Meta:
        model = Word

    content = fake.pystr(min_chars=3, max_chars=10, prefix="CONTENT_")
    style = factory.SubFactory(StyleFactory)


class SigntureFactory(BaseLineElementFactory):
    class Meta:
        model = Signature

    value = fake.pystr(min_chars=3, max_chars=10, prefix="VALUE_")


class SelectionMarkFactory(BaseLineElementFactory):
    class Meta:
        model = SelectionMark

    state = fake.pystr(min_chars=3, max_chars=10, prefix="STATE_")


class FormulaFactory(BaseLineElementFactory):
    class Meta:
        model = Formula

    value = fake.pystr(min_chars=3, max_chars=10, prefix="VALUE_")
    kind = fake.pystr(min_chars=3, max_chars=10, prefix="KIND_")


class BarcodeFactory(BaseLineElementFactory):
    class Meta:
        model = Barcode

    value = fake.ean()
    kind = fake.pystr(min_chars=3, max_chars=10, prefix="KIND_")
