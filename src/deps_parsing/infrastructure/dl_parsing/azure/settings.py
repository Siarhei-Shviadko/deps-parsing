from pydantic import Field
from pydantic_settings import BaseSettings

from .constants import AzureParsingStrategyEnum

__all__ = ["AzureSettings"]


class AzureSettings(BaseSettings):
    parsing_strategy: AzureParsingStrategyEnum = Field(
        AzureParsingStrategyEnum.BY_DOCUMENT,
        validation_alias="AZURE_PARSING_STRATEGY",
    )
