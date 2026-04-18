from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    api_url: str = Field("", validation_alias="AZURE_FORM_RECOGNIZER_API_URL")
    api_key: str = Field("", validation_alias="AZURE_FORM_RECOGNIZER_API_KEY")
