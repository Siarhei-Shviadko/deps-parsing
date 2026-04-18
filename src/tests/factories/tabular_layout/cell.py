from uuid import uuid4

import factory
from deps_tabular_layout.models import Cell, DataType, EntityId

from .alignment import AlignmentFactory
from .borders import BordersFactory
from .comment import CommentFactory
from .merge_info import MergeInfoFactory
from .point import PointFactory
from .style import StyleFactory

__all__ = ["CellFactory"]


class CellFactory(factory.Factory):
    class Meta:
        model = Cell

    id_ = factory.LazyFunction(lambda: EntityId(uuid4().hex))
    table_id = factory.LazyFunction(lambda: EntityId(uuid4().hex))
    content = factory.Faker("sentence")
    relative_position = factory.SubFactory(PointFactory)
    absolute_position = factory.SubFactory(PointFactory)
    data_type = factory.Iterator(
        [
            DataType.STRING,
            DataType.BOOL,
            DataType.FORMULA,
            DataType.NUMERIC,
            DataType.BOOL,
            DataType.ERROR,
            DataType.OTHER,
        ]
    )
    merge = factory.SubFactory(MergeInfoFactory)
    style = factory.SubFactory(StyleFactory)
    comment = factory.SubFactory(CommentFactory)
    alignment = factory.SubFactory(AlignmentFactory)
    borders = factory.SubFactory(BordersFactory)
