from typing import Any

from azure.ai.formrecognizer import DocumentSpan

__all__ = ["SpansOf"]

FIRST_ELEMENT: int = 0


class SpansOf:
    def __init__(self, element: Any) -> None:
        if hasattr(element, "spans") and isinstance(element.spans[FIRST_ELEMENT], DocumentSpan):
            self._spans = list(element.spans)
        elif hasattr(element, "span") and isinstance(element.span, DocumentSpan):
            self._spans = [element.span]
        else:
            raise RuntimeError(f"Incompatible element `{element}` for SpansOf")

    @property
    def spans(self) -> list[DocumentSpan]:
        return self._spans

    def include(self, other: "SpansOf") -> bool:
        for span in self.spans:
            for other_span in other.spans:
                if span.offset <= other_span.offset <= (span.offset + span.length):
                    return True

        return False
