from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from .datasource import DBDialect, DBDriver

__all__ = ["AuthenticationSettings", "Settings", "ServiceInfoSettings", "DatabaseSettings"]


class AuthenticationSettings(BaseSettings):
    enabled: bool = Field(default=False, validation_alias="AUTH_ENABLED")
    verify_ssl: bool = Field(default=True, validation_alias="AUTH_VERIFY_SSL")
    certs_endpoint: str | None = Field(default=None, validation_alias="AUTH_CERTS_ENDPOINT")
    encryption_algorithm: str = Field(default="RS256", validation_alias="AUTH_ENCRYPTION_ALGORITHM")
    api_key: str | None = Field(default=None, validation_alias="API_KEY")

    @model_validator(mode="after")
    def validate_certs_endpoint_and_key(self) -> "AuthenticationSettings":
        if self.enabled and (self.certs_endpoint is None and self.api_key is None):
            raise ValueError(
                "Please provide OAUTH certificates endpoint via `AUTH_CERTS_ENDPOINT` "
                "or provide auth key via `API_KEY`",
            )
        return self


class ServiceInfoSettings(BaseSettings):
    tag: str = ""
    date: str = ""
    hash: str = ""

    model_config = SettingsConfigDict(env_prefix="SERVICE_INFO_")


class Settings(BaseSettings):
    info: ServiceInfoSettings = ServiceInfoSettings()
    auth: AuthenticationSettings = AuthenticationSettings()
    ocr_api_url: str | None = Field(default=None, validation_alias="OCR_API_URL")
    file_storage_url: str | None = Field(default=None, validation_alias="FILE_STORAGE_URL")
    tables_api_url: str | None = Field(default=None, validation_alias="TABLES_API_URL")
    omr_service_url: str | None = Field(default=None, validation_alias="OMR_SERVICE_URL")
    debug_mode: bool = Field(default=False, validation_alias="DEBUG_MODE")


class SSLSettings(BaseSettings):
    key: str = ""
    cert: str = ""
    rootcert: str = ""
    mode: str = "verify-full"

    model_config = SettingsConfigDict(env_prefix="DATABASE_SSL")


class DatabaseSettings(BaseSettings):
    user: str
    password: str
    host: str
    port: str
    db: str
    ssl: SSLSettings = SSLSettings()
    dialect: DBDialect = DBDialect.POSTGRES
    driver: DBDriver = DBDriver.PSYCOPG2
    require_secure_transport: bool = False

    model_config = SettingsConfigDict(env_prefix="DATABASE_")
