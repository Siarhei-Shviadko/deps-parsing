from http import HTTPStatus
from typing import Optional

from deps_document_layout.model import (
    DocumentLayoutFeaturesFilter,
    PageBatch,
    ParsingFeature,
    ParsingType,
)
from fastapi import Query
from fastapi.exceptions import HTTPException

__all__ = ["DocumentLayoutFeaturesFilterFactory"]


class DocumentLayoutFeaturesFilterFactory:
    @classmethod
    def make_base_filter(
        cls,
        parsing_type: ParsingType = Query(..., alias="parsingType"),
        features: Optional[set[ParsingFeature]] = Query(None),
    ) -> DocumentLayoutFeaturesFilter:
        return DocumentLayoutFeaturesFilter(
            parsing_type=parsing_type,
            features=features if features else set(),
        )

    @classmethod
    def make_filter(
        cls,
        parsing_type: ParsingType = Query(..., alias="parsingType"),
        features: Optional[set[ParsingFeature]] = Query(None),
        batch_index: Optional[int] = Query(None, ge=0, alias="batchIndex"),
        batch_size: Optional[int] = Query(None, ge=1, alias="batchSize"),
    ) -> DocumentLayoutFeaturesFilter:
        return DocumentLayoutFeaturesFilter(
            parsing_type=parsing_type,
            features=features if features else set(),
            page_batch=cls._make_pagination(batch_index, batch_size),
        )

    @classmethod
    def make_filter_with_default_pagination(
        cls,
        parsing_type: ParsingType = Query(..., alias="parsingType"),
        features: Optional[set[ParsingFeature]] = Query(None),
        batch_index: int = Query(PageBatch.index, ge=0, alias="batchIndex"),
        batch_size: int = Query(PageBatch.size, ge=1, alias="batchSize"),
    ) -> DocumentLayoutFeaturesFilter:
        return DocumentLayoutFeaturesFilter(
            parsing_type=parsing_type,
            features=features if features else set(),
            page_batch=cls._make_pagination(batch_index, batch_size),
        )

    @classmethod
    def _make_pagination(cls, batch_index: Optional[int], batch_size: Optional[int]) -> Optional[PageBatch]:
        if (batch_index is None) != (batch_size is None):
            raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="Pagination is invalid.")

        return PageBatch(index=batch_index, size=batch_size) if batch_size is not None else None
