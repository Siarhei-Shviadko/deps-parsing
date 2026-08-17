from typing import Any

from deps_asb import ASBSettings
from deps_kafka import KafkaSettings
from deps_message_flow import MessagingDriverEnum
from deps_rabbitmq import RabbitMQTLSSettings
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from deps_parsing.domain.constants import ABSENCE, PRESENCE
from deps_parsing.domain.services.split_tables_detection import (
    SimilarityMarkers,
    SimilarityMarkersWeight,
)
from deps_parsing.extras.settings import (
    AuthenticationSettings,
    DatabaseSettings,
    ServiceInfoSettings,
)
from deps_parsing.infrastructure.dl_parsing import (
    AWSTextractConfig,
    AzureSettings,
    GCPDocumentAISettings,
)


class MergeTablesSettings(BaseSettings):
    similarity_threshold: float = Field(
        default=SimilarityMarkersWeight.calculate_default_threshold(),
        validation_alias="MERGED_TABLES_SIMILARITY_THRESHOLD",
    )
    weights: dict[SimilarityMarkers, dict[bool, float]] = Field(
        default_factory=SimilarityMarkersWeight.make_default_weights,
        validation_alias="MERGED_TABLES_WEIGHTS",
    )
    enabled: bool = Field(default=True, validation_alias="MERGE_TABLES_ENABLED")

    @classmethod
    @field_validator("weights")
    def validate_weights(
        cls,
        weights: dict[SimilarityMarkers, dict[bool, float]],
    ) -> dict[SimilarityMarkers, dict[bool, float]]:
        for marker_weight in weights.values():
            if PRESENCE not in marker_weight:
                marker_weight[PRESENCE] = 0
            if ABSENCE not in marker_weight:
                marker_weight[ABSENCE] = 0

        return weights


class UnifierProxySettings(BaseSettings):
    url: str
    proxy_timeout: int = 60

    model_config = SettingsConfigDict(env_prefix="UNIFIER_")


class AIFusionProxySettings(BaseSettings):
    url: str
    proxy_timeout: int = 120

    model_config = SettingsConfigDict(env_prefix="AI_FUSION_")


class OCRProxySettings(BaseSettings):
    url: str
    proxy_timeout: int = 300

    model_config = SettingsConfigDict(env_prefix="OCR_")


class TablesProxySettings(BaseSettings):
    url: str
    proxy_timeout: int = 300

    model_config = SettingsConfigDict(env_prefix="TABLES_")


class DocumentProxySettings(BaseSettings):
    url: str
    proxy_timeout: int = 60

    model_config = SettingsConfigDict(env_prefix="DOCUMENT_")


class FileProxySettings(BaseSettings):
    url: str
    proxy_timeout: int = 60

    model_config = SettingsConfigDict(env_prefix="FILE_")


class SemanticParsingProxySettings(BaseSettings):
    url: str = ""
    proxy_timeout: int = 60

    model_config = SettingsConfigDict(env_prefix="SEMANTIC_PARSING_")


class Settings(BaseSettings):
    env: str = "development"
    version: str = "1.0"

    logger_level: str = Field("INFO", validation_alias="LOG_LEVEL")

    info: ServiceInfoSettings = ServiceInfoSettings()
    database: DatabaseSettings = DatabaseSettings()
    authentication: AuthenticationSettings = AuthenticationSettings()
    unifier: UnifierProxySettings = UnifierProxySettings()
    ocr: OCRProxySettings = OCRProxySettings()
    tables: TablesProxySettings = TablesProxySettings()
    document: DocumentProxySettings = DocumentProxySettings()
    file: FileProxySettings = FileProxySettings()
    semantic_parsing: SemanticParsingProxySettings = SemanticParsingProxySettings()
    ai_fusion: AIFusionProxySettings = AIFusionProxySettings()

    messaging_driver: MessagingDriverEnum = Field(MessagingDriverEnum.RABBITMQ, validation_alias="MESSAGING_DRIVER")
    messaging_driver_settings: Any = Field(None, validation_alias="MESSAGING_DRIVER_SETTINGS")
    message_broker_connection_string: str

    documentation_enabled: bool = True
    instrumentation_enabled: bool = False
    semantic_layout_enabled: bool = Field(default=False, validation_alias="SEMANTIC_LAYOUT_ENABLED")

    raw_file_extension: str = "json"

    aws_textract: AWSTextractConfig = AWSTextractConfig()
    gcp_document_ai: GCPDocumentAISettings = GCPDocumentAISettings()

    ssl_verify: bool = False

    azure_dl_parsing: AzureSettings = AzureSettings()

    default_ocr_engine: str = "TESSERACT"
    merge_tables_settings: MergeTablesSettings = MergeTablesSettings()

    model_config = SettingsConfigDict(use_enum_values=True)

    @classmethod
    @field_validator("messaging_driver_settings")
    def validate_messaging_driver_settings(cls, v, info):  # noqa: N805
        messaging_driver = info.data.get("messaging_driver")
        if not messaging_driver:
            raise ValueError("Invalid messaging driver")

        driver = MessagingDriverEnum(messaging_driver)
        if driver == MessagingDriverEnum.ASB:
            return ASBSettings()
        elif driver == MessagingDriverEnum.KAFKA:
            return KafkaSettings()
        elif driver == MessagingDriverEnum.RABBITMQ:
            return RabbitMQTLSSettings().model_dump()  # TODO: use BaseSettings

        raise ValueError(f"Driver {driver} is not implemented")
