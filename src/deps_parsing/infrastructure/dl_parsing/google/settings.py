from enum import Enum

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

__all__ = ["GCPDocumentAISettings", "GCPDocumentAIParsingStrategyEnum"]


class GCPDocumentAIParsingStrategyEnum(str, Enum):
    BY_PAGE = "by_page"
    BY_DOCUMENT = "by_document"


class GCPDocumentAISettings(BaseSettings):
    project_id: str = ""
    location: str = "eu"

    form_recognition_processor_id: str = ""

    account_info_json: str = Field(
        default="",
        description="Can be either a JSON string of Service Account or Workload Identity Federation JSON config",
    )

    idp_token_url: str = ""
    idp_client_id: str = ""
    idp_client_secret: str = ""

    parsing_strategy: GCPDocumentAIParsingStrategyEnum = Field(GCPDocumentAIParsingStrategyEnum.BY_DOCUMENT)
    output_directory_path: str = ""

    model_config = SettingsConfigDict(env_prefix="GCP_DOCAI_")
