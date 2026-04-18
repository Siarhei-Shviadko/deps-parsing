from pydantic import Field

from deps_parsing.domain.dtos import PageInfo

from ....base import ConfiguredBaseModel

__all__ = ["SerializedPageInfo"]


class SerializedPageInfo(ConfiguredBaseModel):
    pages_count: int = Field(..., alias="pagesCount")

    @classmethod
    def from_model(cls, page_info: PageInfo) -> "SerializedPageInfo":
        return cls(pages_count=page_info.pages_count)
