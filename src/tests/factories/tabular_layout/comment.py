import factory
from deps_tabular_layout.models import Comment

__all__ = ["CommentFactory"]


class CommentFactory(factory.Factory):
    class Meta:
        model = Comment

    author = factory.Faker("name")
    content = factory.Faker("sentence")
