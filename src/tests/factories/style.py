import factory
from deps_document_layout.model import Style
from faker import Faker

__all__ = ["StyleFactory"]

fake = Faker()


class StyleFactory(factory.Factory):
    class Meta:
        model = Style

    background_color = fake.safe_color_name()
    color = fake.safe_color_name()
    bold = fake.pybool()
    italic = fake.pybool()
    handwritten = fake.pybool()
    font_type = fake.language_name()
    font_size = fake.language_name()
    underlined = fake.pybool()
    strikeout = fake.pybool()
    subscript = fake.pybool()
    superscript = fake.pybool()
    smallcaps = fake.pybool()
