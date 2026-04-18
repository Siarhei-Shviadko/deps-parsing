from enum import Enum

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

__all__ = ["AWSTextractConfig", "AWSTextractParsingStrategyEnum"]


class AWSTextractParsingStrategyEnum(str, Enum):
    BY_PAGE = "by_page"
    BY_DOCUMENT = "by_document"


class AWSTextractConfig(BaseSettings):
    region_name: str = "eu-central-1"
    access_key_id: str = ""
    secret_access_key: str = ""
    parsing_strategy: AWSTextractParsingStrategyEnum = Field(AWSTextractParsingStrategyEnum.BY_DOCUMENT)
    parallelism_factor: int = Field(5)

    s3_bucket_name: str = Field("", validation_alias="S3_BUCKET_NAME")

    model_config = SettingsConfigDict(env_prefix="AWS_TEXTRACT_")

    @classmethod
    @field_validator("region_name")
    def region_name_use_default_if_empty(cls, value: str) -> str:
        if value == "":
            return "eu-central-1"
        return value
