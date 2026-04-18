import factory
from deps_tabular_layout.models import Style

__all__ = ["StyleFactory"]


class StyleFactory(factory.Factory):
    class Meta:
        model = Style

    background_color = factory.Faker("color")
    color = factory.Faker("word")
    hyperlink = factory.Faker("pybool")
    bold = factory.Faker("pybool")
    italic = factory.Faker("pybool")
    font_name = factory.Faker("word")
    font_size = factory.Faker("word")
    underlined = factory.Faker("pybool")
    strikethrough = factory.Faker("pybool")
