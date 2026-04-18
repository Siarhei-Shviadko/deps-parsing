from azure.ai.formrecognizer import DocumentKeyValueElement

from .checkmarks import AzureCheckmarksMap

__all__ = ["ValueResponse"]


class ValueResponse:
    @classmethod
    def with_value(cls, value: DocumentKeyValueElement) -> DocumentKeyValueElement:
        if cls._is_checkmark_value(value):
            return DocumentKeyValueElement(
                content=AzureCheckmarksMap[value.content],
                bounding_regions=value.bounding_regions,
                spans=value.spans,
            )

        return value

    @staticmethod
    def _is_checkmark_value(value: DocumentKeyValueElement) -> bool:
        return value.content in AzureCheckmarksMap
