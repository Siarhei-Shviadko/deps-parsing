from pydantic import BaseModel
from pydantic_settings import SettingsConfigDict

__all__ = ["ConfiguredBaseModel"]


class ConfiguredBaseModel(BaseModel):
    model_config = SettingsConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )
