from deps_tabular_layout.models import Comment

__all__ = ["CommentMapper"]


class CommentMapper:
    @staticmethod
    def to_dict(comment: Comment) -> dict[str, str]:
        return {
            "author": comment.author,
            "content": comment.content,
        }

    @staticmethod
    def from_raw(raw_comment: dict[str, str]) -> Comment:
        return Comment(
            author=raw_comment["author"],
            content=raw_comment["content"],
        )
