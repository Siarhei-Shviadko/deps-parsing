import factory
from deps_tabular_layout.models import MergeInfo

__all__ = ["MergeInfoFactory"]


class MergeInfoFactory(factory.Factory):
    class Meta:
        model = MergeInfo

    column_span = factory.Faker("pyint", min_value=1, max_value=3)
    row_span = factory.Faker("pyint", min_value=1, max_value=3)
