import factory
from deps_document_layout.model import Line
from faker import Faker

from .line_elements import (
    BarcodeFactory,
    FormulaFactory,
    SelectionMarkFactory,
    SigntureFactory,
    WordFactory,
)
from .polygon import PolygonFactory

__all__ = ["LineFactory"]

fake = Faker()


class LineFactory(factory.Factory):
    class Meta:
        model = Line

    order = fake.pyint()
    content = fake.pystr(min_chars=3, max_chars=10, prefix="CONTENT_")
    confidence = fake.pyfloat(min_value=0, max_value=1)
    polygon = factory.SubFactory(PolygonFactory)

    words = factory.LazyFunction(lambda: tuple(WordFactory() for _ in range(fake.pyint(max_value=10))))
    selection_marks = factory.LazyFunction(
        lambda: tuple(SelectionMarkFactory() for _ in range(fake.pyint(max_value=10)))
    )
    barcodes = factory.LazyFunction(lambda: tuple(BarcodeFactory() for _ in range(fake.pyint(max_value=10))))
    formulas = factory.LazyFunction(lambda: tuple(FormulaFactory() for _ in range(fake.pyint(max_value=10))))
    signatures = factory.LazyFunction(lambda: tuple(SigntureFactory() for _ in range(fake.pyint(max_value=10))))
