import random

import factory
from deps_document_layout.model import Blurring, Thresholding, Transformations
from faker import Faker

__all__ = ["TransformationsFactory"]

fake = Faker()


class BlurringFactory(factory.Factory):
    class Meta:
        model = Blurring

    kernel = factory.LazyFunction(lambda: tuple([fake.pyint(max_value=100), fake.pyint(max_value=100)]))
    sigma = fake.pyfloat()


class ThresholdingFactory(factory.Factory):
    class Meta:
        model = Thresholding

    low_value = fake.pyint(max_value=100)
    high_value = factory.LazyAttribute(lambda o: fake.pyint(min_value=o.low_value, max_value=o.low_value + 100))
    flag = fake.pyint(max_value=100)


class TransformationsFactory(factory.Factory):
    class Meta:
        model = Transformations

    blurring = factory.LazyFunction(lambda: BlurringFactory() if fake.pybool() else None)
    grayscaling = fake.pybool()
    orientation = random.choice([fake.pystr(min_chars=3, max_chars=5, prefix="Orientation_"), None])
    angle = random.choice([fake.pyfloat(), None])
    thresholding = factory.SubFactory(ThresholdingFactory)
