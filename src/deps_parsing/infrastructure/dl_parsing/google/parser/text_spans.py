from .types import DocAILayout

__all__ = ["TextSpans"]


class TextSpans:
    def __init__(self, target: DocAILayout) -> None:
        self._target = target

        self.target_lower_bound = target.text_anchor.text_segments[0].start_index
        self.target_upper_bound = target.text_anchor.text_segments[-1].end_index

    @classmethod
    def for_layout(cls, target: DocAILayout) -> "TextSpans":
        return cls(target)

    def lies_below(self, other: DocAILayout) -> bool:
        """Checks if the target text segments are lying below the other text block on the page."""
        return self.target_lower_bound > other.text_anchor.text_segments[0].start_index

    def includes(self, other: DocAILayout) -> bool:
        """Checks if the target text segments are including the other text block."""
        return (
            self.target_lower_bound <= other.text_anchor.text_segments[0].start_index
            and other.text_anchor.text_segments[-1].end_index <= self.target_upper_bound
        )
