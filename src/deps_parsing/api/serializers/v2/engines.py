from pydantic import Field

from deps_parsing.application import LayoutType

from ..base import ConfiguredBaseModel

__all__ = ["EngineSerializer", "EnginesResponse"]


class EngineSerializer(ConfiguredBaseModel):
    code: str
    name: str
    layout_type: LayoutType = Field(..., alias="layoutType")


class EnginesResponse(ConfiguredBaseModel):
    engines: list[EngineSerializer]
