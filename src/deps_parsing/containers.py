from typing import Any, Optional, Type, Union

from dependency_injector import containers, providers, resources
from deps_asb import ASBClient, ASBConsumer, ASBProducer
from deps_document_layout.model import IDocumentLayoutRepository
from deps_document_layout.model import ParsingType as DLParsingType
from deps_kafka import KafkaClient, KafkaConsumer, KafkaProducer
from deps_message_flow import MessagingDriverEnum
from deps_message_flow.commands.producer import CommandProducer
from deps_message_flow.events.publisher import DomainEventPublisher
from deps_message_flow.messaging.consumer import IMessageConsumer
from deps_message_flow.messaging.producer import IMessageProducer
from deps_message_flow.sagas.orchestration import (
    SagaCommandProducer,
    SagaDataMapping,
    SagaInstanceFactory,
    SagaManagerFactory,
)
from deps_object_storage import ObjectStorage, make_object_storage
from deps_rabbitmq import RabbitMQClient, RabbitMQConsumer, RabbitMQProducer
from deps_tabular_layout.models import ParsingType as TLParsingType

from deps_parsing.application import (
    DocumentLayoutService,
    DocumentTypeService,
    ParsingService,
    SemanticLayoutService,
    StubSemanticLayoutService,
    TabularLayoutService,
)
from deps_parsing.application.v2 import (
    DocumentLayoutServiceV2,
    ParsingServiceV2,
    SemanticLayoutApplicationV2,
    StubSemanticLayoutApplicationV2,
    TabularLayoutServiceV2,
)
from deps_parsing.constants import PROJECT_NAME
from deps_parsing.domain.interfaces import (
    ICellCommandRepository,
    IRawDocumentLayoutRepository,
    ITabularLayoutCommandRepository,
    ITabularLayoutQueryRepository,
)
from deps_parsing.domain.model import IDocumentTypeRepository
from deps_parsing.domain.services import SplitTablesDetectionService
from deps_parsing.extras.datasource import Database
from deps_parsing.extras.datasource.constants import DBDialect, DBDriver
from deps_parsing.infrastructure import AWSTextractProxy, GCPDocumentAIProxy
from deps_parsing.infrastructure.access_management import user
from deps_parsing.infrastructure.dl_parsing import (
    AWSTextractDocumentParsingService,
    AWSTextractEngine,
    AWSTextractPageParsingService,
    AzureDocumentParsingService,
    AzureOCREngine,
    AzurePageParsingService,
    CraftTesseractParsingEngine,
    CraftTesseractParsingService,
    DocumentAIDocumentParsingService,
    DocumentAIEngine,
    DocumentAIPageParsingService,
    DOCXParsingService,
    EasyocrParsingEngine,
    EasyocrParsingService,
    OCRLayoutImageProcessingService,
    PaddleocrParsingEngine,
    PaddleocrParsingService,
    TesseractParsingEngine,
    TesseractParsingService,
)
from deps_parsing.infrastructure.dl_parsing.v2 import (
    AWSTextractDocumentParsingServiceV2,
    AWSTextractPageParsingServiceV2,
    AzureDocumentParsingServiceV2,
    AzurePageParsingServiceV2,
    DocumentAIDocumentParsingServiceV2,
    DocumentAIPageParsingServiceV2,
    DOCXParsingServiceV2,
    TesseractParsingServiceV2,
)
from deps_parsing.infrastructure.proxies import (
    AIFusionProxy,
    AzureDocumentIntelligenceProxy,
    DocumentProxy,
    FileProxy,
    OCRProxy,
    SemanticParsingProxy,
    TablesProxy,
    UnifierProxy,
)
from deps_parsing.infrastructure.repositories import (
    CellCommandRepository,
    DocumentLayoutRepository,
    DocumentTypeRepository,
    RawDocumentLayoutRepository,
    SagaInstanceRepository,
    TabularLayoutCommandRepository,
    TabularLayoutQueryRepository,
)
from deps_parsing.infrastructure.tl_parsing import CSVParser, ExcelParser
from deps_parsing.infrastructure.tl_parsing.v2 import CSVParserV2, ExcelParserV2
from deps_parsing.messaging.dispatcher import make_message_dispatcher
from deps_parsing.messaging.sagas import PageParsingSaga
from deps_parsing.messaging.sagas_data import PageParsingSteps, make_saga_data_mapping

MessagingClient = Union[ASBClient, KafkaClient, RabbitMQClient]


class DatabaseResource(resources.Resource):
    def init(
        self,
        username: str,
        password: str,
        host: str,
        port: int,
        database: str,
        dialect: DBDialect,
        driver: DBDriver,
        require_secure_transport: bool,
    ) -> Database:
        db = Database(
            username=username,
            password=password,
            host=host,
            port=port,
            database=database,
            dialect=dialect,
            driver=driver,
            require_secure_transport=require_secure_transport,
        )
        db.connect()
        return db

    def shutdown(self, resource: Database) -> None:
        resource.close()


class MessageBrokerResource(resources.Resource):
    def init(
        self,
        driver_type: str,
        expected_driver: str,
        client: Type[MessagingClient],
        message_connection_string: str,
        **kwargs: dict[str, Any],
    ) -> Optional[MessagingClient]:
        return client(message_connection_string, **kwargs) if driver_type == expected_driver else None

    def shutdown(self, resource: Optional[MessagingClient]) -> None:
        if resource:
            resource.close()


class MessageBrokers(containers.DeclarativeContainer):
    config = providers.Configuration()
    messaging_driver_settings = providers.Dependency(instance_of=object)

    broker_client: providers.Provider[MessagingClient] = providers.Selector(
        config.messaging_driver,
        asb=providers.Resource(
            MessageBrokerResource,
            driver_type=MessagingDriverEnum.ASB.value,
            expected_driver=config.messaging_driver,
            client=ASBClient,
            message_connection_string=config.message_broker_connection_string,
            asb_settings=messaging_driver_settings,
        ),
        kafka=providers.Resource(
            MessageBrokerResource,
            driver_type=MessagingDriverEnum.KAFKA.value,
            expected_driver=config.messaging_driver,
            client=KafkaClient,
            message_connection_string=config.message_broker_connection_string,
            settings=messaging_driver_settings,
        ),
        rabbitmq=providers.Resource(
            MessageBrokerResource,
            driver_type=MessagingDriverEnum.RABBITMQ.value,
            expected_driver=config.messaging_driver,
            client=RabbitMQClient,
            message_connection_string=config.message_broker_connection_string,
            settings=messaging_driver_settings,
        ),
    )


class Messaging(containers.DeclarativeContainer):
    config = providers.Configuration()
    message_brokers = providers.DependenciesContainer()

    producer: providers.Provider[IMessageProducer] = providers.Selector(
        config.messaging_driver,
        asb=providers.Singleton(
            ASBProducer,
            client=message_brokers.broker_client,
            topic_name=config.messaging_driver_settings.topic_name,
        ),
        kafka=providers.Singleton(
            KafkaProducer,
            client=message_brokers.broker_client,
        ),
        rabbitmq=providers.Singleton(
            RabbitMQProducer,
            client=message_brokers.broker_client,
        ),
    )
    consumer: providers.Provider[IMessageConsumer] = providers.Selector(
        config.messaging_driver,
        asb=providers.Singleton(
            ASBConsumer,
            client=message_brokers.broker_client,
            topic_name=config.messaging_driver_settings.topic_name,
            custom_subscription_name=PROJECT_NAME,
        ),
        kafka=providers.Singleton(
            KafkaConsumer,
            client=message_brokers.broker_client,
        ),
        rabbitmq=providers.Singleton(
            RabbitMQConsumer,
            client=message_brokers.broker_client,
        ),
    )


class Core(containers.DeclarativeContainer):
    config = providers.Configuration()
    build_info: providers.Provider[dict] = providers.Dict(
        {
            "build_tag": config.info.tag,
            "build_date": config.info.date,
            "commit_hash": config.info.hash,
        },
    )


class Datasources(containers.DeclarativeContainer):
    config = providers.Configuration()

    postgres_datasource: providers.Provider[Database] = providers.Resource(
        DatabaseResource,
        config.user,
        config.password,
        config.host,
        config.port,
        config.db,
        config.dialect,
        config.driver,
        config.require_secure_transport,
    )


class ExternalServices(containers.DeclarativeContainer):
    config = providers.Configuration()

    object_storage: providers.Provider[ObjectStorage] = providers.Singleton(make_object_storage)

    unifier: providers.Provider[UnifierProxy] = providers.Singleton(
        UnifierProxy,
        base_url=config.unifier.url,
        timeout=config.unifier.proxy_timeout,
        ssl_verify=config.ssl_verify,
    )
    tables: providers.Provider[TablesProxy] = providers.Singleton(
        TablesProxy,
        base_url=config.tables.url,
        timeout=config.tables.proxy_timeout,
        ssl_verify=config.ssl_verify,
    )
    ocr: providers.Provider[OCRProxy] = providers.Singleton(
        OCRProxy,
        base_url=config.ocr.url,
        timeout=config.ocr.proxy_timeout,
        ssl_verify=config.ssl_verify,
    )
    document: providers.Provider[DocumentProxy] = providers.Singleton(
        DocumentProxy,
        base_url=config.document.url,
        timeout=config.document.proxy_timeout,
        ssl_verify=config.ssl_verify,
    )
    file: providers.Provider[FileProxy] = providers.Singleton(
        FileProxy,
        base_url=config.file.url,
        timeout=config.file.proxy_timeout,
        ssl_verify=config.ssl_verify,
    )
    ai_fusion: providers.Provider[AIFusionProxy] = providers.Singleton(
        AIFusionProxy,
        base_url=config.ai_fusion.url,
        timeout=config.ai_fusion.proxy_timeout,
        ssl_verify=config.ssl_verify,
    )
    semantic_parsing: providers.Provider[SemanticParsingProxy] = providers.Singleton(
        SemanticParsingProxy,
        base_url=config.semantic_parsing.url,
        timeout=config.semantic_parsing.proxy_timeout,
        ssl_verify=config.ssl_verify,
    )

    azure: providers.Provider[AzureDocumentIntelligenceProxy] = providers.Singleton(
        AzureDocumentIntelligenceProxy,
    )
    aws_textract: providers.Provider[AWSTextractProxy] = providers.Singleton(
        AWSTextractProxy,
        region_name=config.aws_textract.region_name,
        aws_access_key_id=config.aws_textract.access_key_id,
        aws_secret_access_key=config.aws_textract.secret_access_key,
    )
    gcp_document_ai: providers.Provider[GCPDocumentAIProxy] = providers.Singleton(
        GCPDocumentAIProxy,
        config=config.gcp_document_ai,
    )


class Engines(containers.DeclarativeContainer):
    external_services = providers.DependenciesContainer()
    sagas: providers.Dependency[providers.List] = providers.Dependency()
    saga_instance_factory: providers.Dependency[SagaInstanceFactory] = providers.Dependency()

    azure: providers.Provider[AzureOCREngine] = providers.Singleton(
        AzureOCREngine,
        proxy=external_services.azure,
    )
    aws_textract: providers.Provider[AWSTextractEngine] = providers.Singleton(
        AWSTextractEngine,
        aws_textract_proxy=external_services.aws_textract,
    )
    document_ai: providers.Provider[DocumentAIEngine] = providers.Singleton(
        DocumentAIEngine,
        document_ai_proxy=external_services.gcp_document_ai,
    )
    tesseract: providers.Provider[TesseractParsingEngine] = providers.Singleton(
        TesseractParsingEngine,
        sagas=sagas,
        saga_factory=saga_instance_factory,
    )
    easy_ocr: providers.Provider[EasyocrParsingEngine] = providers.Singleton(
        EasyocrParsingEngine,
        sagas=sagas,
        saga_factory=saga_instance_factory,
    )
    craft_tesseract: providers.Provider[CraftTesseractParsingEngine] = providers.Singleton(
        CraftTesseractParsingEngine,
        sagas=sagas,
        saga_factory=saga_instance_factory,
    )
    paddle_ocr: providers.Provider[PaddleocrParsingEngine] = providers.Singleton(
        PaddleocrParsingEngine,
        sagas=sagas,
        saga_factory=saga_instance_factory,
    )


class Repositories(containers.DeclarativeContainer):
    config = providers.Configuration()
    datasources = providers.DependenciesContainer()
    external_services = providers.DependenciesContainer()

    raw_document_layout: providers.Singleton[IRawDocumentLayoutRepository] = providers.Singleton(
        RawDocumentLayoutRepository,
        object_storage=external_services.object_storage,
        file_extension=config.raw_file_extension,
    )
    document_layout: providers.Singleton[IDocumentLayoutRepository] = providers.Singleton(
        DocumentLayoutRepository,
        database=datasources.postgres_datasource,
    )
    document_type: providers.Singleton[IDocumentTypeRepository] = providers.Singleton(
        DocumentTypeRepository,
        database=datasources.postgres_datasource,
    )
    saga_instance: providers.Provider[SagaInstanceRepository] = providers.Singleton(
        SagaInstanceRepository,
        database=datasources.postgres_datasource,
    )
    tabular_layout_query: providers.Provider[ITabularLayoutQueryRepository] = providers.Singleton(
        TabularLayoutQueryRepository,
        database=datasources.postgres_datasource,
    )
    tabular_layout_command: providers.Singleton[ITabularLayoutCommandRepository] = providers.Singleton(
        TabularLayoutCommandRepository,
        database=datasources.postgres_datasource,
    )
    cell_command: providers.Singleton[ICellCommandRepository] = providers.Singleton(
        CellCommandRepository,
        database=datasources.postgres_datasource,
    )


class SagaSteps(containers.DeclarativeContainer):
    external_services = providers.DependenciesContainer()

    page_parsing: providers.Singleton[PageParsingSteps] = providers.Singleton(
        PageParsingSteps,
        ocr_proxy=external_services.ocr,
        tables_proxy=external_services.tables,
    )


class DomainServices(containers.DeclarativeContainer):
    config = providers.Configuration()

    split_tables_detector: providers.Singleton[SplitTablesDetectionService] = providers.Singleton(
        SplitTablesDetectionService,
        similarity_threshold=config.merge_tables_settings.similarity_threshold,
        weights=config.merge_tables_settings.weights,
    )


class Applications(containers.DeclarativeContainer):
    config = providers.Configuration()
    engines = providers.DependenciesContainer()
    domain_services = providers.DependenciesContainer()
    external_services = providers.DependenciesContainer()
    repositories = providers.DependenciesContainer()
    command_producer: providers.Dependency = providers.Dependency()
    domain_event_publisher: providers.Dependency = providers.Dependency()

    ocr_image_preprocessing_service: providers.Singleton[OCRLayoutImageProcessingService] = providers.Singleton(
        OCRLayoutImageProcessingService,
        storage=external_services.object_storage,
        image_recognizer=external_services.ai_fusion,
    )

    tabular_layout_service: providers.Singleton[TabularLayoutService] = providers.Singleton(
        TabularLayoutService,
        tl_query_repository=repositories.tabular_layout_query,
        parsing_service_mapper=providers.Dict(
            {
                TLParsingType.EXCEL: providers.Singleton(
                    ExcelParser,
                    documents_proxy=external_services.document,
                    cell_command_repository=repositories.cell_command,
                ),
                TLParsingType.CSV: providers.Singleton(
                    CSVParser,
                    documents_proxy=external_services.document,
                    cell_command_repository=repositories.cell_command,
                ),
            },
        ),
        tl_command_repository=repositories.tabular_layout_command,
        cell_command_repository=repositories.cell_command,
        domain_event_publisher=domain_event_publisher,
    )

    tabular_layout_service_v2: providers.Singleton[TabularLayoutServiceV2] = providers.Singleton(
        TabularLayoutServiceV2,
        tl_query_repository=repositories.tabular_layout_query,
        parsing_service_mapper=providers.Dict(
            {
                TLParsingType.EXCEL: providers.Singleton(
                    ExcelParserV2,
                    storage=external_services.object_storage,
                    cell_command_repository=repositories.cell_command,
                ),
                TLParsingType.CSV: providers.Singleton(
                    CSVParserV2,
                    storage=external_services.object_storage,
                    cell_command_repository=repositories.cell_command,
                ),
            },
        ),
        tl_command_repository=repositories.tabular_layout_command,
        cell_command_repository=repositories.cell_command,
        domain_event_publisher=domain_event_publisher,
    )

    document_layout_service: providers.Singleton[DocumentLayoutService] = providers.Singleton(
        DocumentLayoutService,
        parsing_service_mapper=providers.Dict(
            {
                DLParsingType.AZURE_FORM_RECOGNIZER: providers.Selector(
                    config.azure_dl_parsing.parsing_strategy,
                    by_page=providers.Singleton(
                        AzurePageParsingService,
                        unifier=external_services.unifier,
                        storage=external_services.object_storage,
                        engine=engines.azure,
                        image_processing_service=ocr_image_preprocessing_service,
                    ),
                    by_document=providers.Singleton(
                        AzureDocumentParsingService,
                        unifier=external_services.unifier,
                        storage=external_services.object_storage,
                        engine=engines.azure,
                        image_processing_service=ocr_image_preprocessing_service,
                        document=external_services.document,
                        file=external_services.file,
                    ),
                ),
                DLParsingType.TESSERACT: providers.Singleton(
                    TesseractParsingService,
                    unifier=external_services.unifier,
                    storage=external_services.object_storage,
                    engine=engines.tesseract,
                    image_processing_service=ocr_image_preprocessing_service,
                ),
                DLParsingType.CRAFT_TESSERACT: providers.Singleton(
                    CraftTesseractParsingService,
                    unifier=external_services.unifier,
                    storage=external_services.object_storage,
                    engine=engines.craft_tesseract,
                    image_processing_service=ocr_image_preprocessing_service,
                ),
                DLParsingType.EASYOCR: providers.Singleton(
                    EasyocrParsingService,
                    unifier=external_services.unifier,
                    storage=external_services.object_storage,
                    engine=engines.easy_ocr,
                    image_processing_service=ocr_image_preprocessing_service,
                ),
                DLParsingType.PADDLEOCR: providers.Singleton(
                    PaddleocrParsingService,
                    unifier=external_services.unifier,
                    storage=external_services.object_storage,
                    engine=engines.paddle_ocr,
                    image_processing_service=ocr_image_preprocessing_service,
                ),
                DLParsingType.AWS_TEXTRACT: providers.Selector(
                    config.aws_textract.parsing_strategy,
                    by_page=providers.Singleton(
                        AWSTextractPageParsingService,
                        unifier=external_services.unifier,
                        storage=external_services.object_storage,
                        engine=engines.aws_textract,
                        image_processing_service=ocr_image_preprocessing_service,
                    ),
                    by_document=providers.Singleton(
                        AWSTextractDocumentParsingService,
                        unifier=external_services.unifier,
                        storage=external_services.object_storage,
                        engine=engines.aws_textract,
                        image_processing_service=ocr_image_preprocessing_service,
                        document=external_services.document,
                        file=external_services.file,
                        s3_bucket_name=config.aws_textract.s3_bucket_name,
                        parallelism_factor=config.aws_textract.parallelism_factor,
                    ),
                ),
                DLParsingType.DOCX: providers.Singleton(
                    DOCXParsingService,
                    documents_proxy=external_services.document,
                ),
                DLParsingType.GCP_VISION: providers.Selector(
                    config.gcp_document_ai.parsing_strategy,
                    by_page=providers.Singleton(
                        DocumentAIPageParsingService,
                        unifier=external_services.unifier,
                        storage=external_services.object_storage,
                        engine=engines.document_ai,
                        image_processing_service=ocr_image_preprocessing_service,
                    ),
                    by_document=providers.Singleton(
                        DocumentAIDocumentParsingService,
                        unifier=external_services.unifier,
                        storage=external_services.object_storage,
                        engine=engines.document_ai,
                        image_processing_service=ocr_image_preprocessing_service,
                        document=external_services.document,
                        file=external_services.file,
                        output_directory=config.gcp_document_ai.output_directory_path,
                    ),
                ),
            },
        ),
        split_tables_detector=domain_services.split_tables_detector,
        document_layout_repository=repositories.document_layout,
        raw_document_layout_repository=repositories.raw_document_layout,
        document_type_repository=repositories.document_type,
        command_producer=command_producer,
        merge_tables_enabled=config.merge_tables_settings.enabled,
    )

    document_layout_service_v2: providers.Singleton[DocumentLayoutServiceV2] = providers.Singleton(
        DocumentLayoutServiceV2,
        parsing_service_mapper=providers.Dict(
            {
                DLParsingType.TESSERACT: providers.Singleton(
                    TesseractParsingServiceV2,
                    unifier=external_services.unifier,
                    storage=external_services.object_storage,
                    engine=engines.tesseract,
                    image_processing_service=ocr_image_preprocessing_service,
                ),
                DLParsingType.AZURE_FORM_RECOGNIZER: providers.Selector(
                    config.azure_dl_parsing.parsing_strategy,
                    by_page=providers.Singleton(
                        AzurePageParsingServiceV2,
                        unifier=external_services.unifier,
                        storage=external_services.object_storage,
                        engine=engines.azure,
                        image_processing_service=ocr_image_preprocessing_service,
                    ),
                    by_document=providers.Singleton(
                        AzureDocumentParsingServiceV2,
                        unifier=external_services.unifier,
                        storage=external_services.object_storage,
                        engine=engines.azure,
                        image_processing_service=ocr_image_preprocessing_service,
                    ),
                ),
                DLParsingType.AWS_TEXTRACT: providers.Selector(
                    config.aws_textract.parsing_strategy,
                    by_page=providers.Singleton(
                        AWSTextractPageParsingServiceV2,
                        unifier=external_services.unifier,
                        storage=external_services.object_storage,
                        engine=engines.aws_textract,
                        image_processing_service=ocr_image_preprocessing_service,
                    ),
                    by_document=providers.Singleton(
                        AWSTextractDocumentParsingServiceV2,
                        unifier=external_services.unifier,
                        storage=external_services.object_storage,
                        engine=engines.aws_textract,
                        image_processing_service=ocr_image_preprocessing_service,
                        s3_bucket_name=config.aws_textract.s3_bucket_name,
                        parallelism_factor=config.aws_textract.parallelism_factor,
                    ),
                ),
                DLParsingType.GCP_VISION: providers.Selector(
                    config.gcp_document_ai.parsing_strategy,
                    by_page=providers.Singleton(
                        DocumentAIPageParsingServiceV2,
                        unifier=external_services.unifier,
                        storage=external_services.object_storage,
                        engine=engines.document_ai,
                        image_processing_service=ocr_image_preprocessing_service,
                    ),
                    by_document=providers.Singleton(
                        DocumentAIDocumentParsingServiceV2,
                        unifier=external_services.unifier,
                        storage=external_services.object_storage,
                        engine=engines.document_ai,
                        image_processing_service=ocr_image_preprocessing_service,
                        output_directory=config.gcp_document_ai.output_directory_path,
                    ),
                ),
                DLParsingType.DOCX: providers.Singleton(
                    DOCXParsingServiceV2,
                    storage=external_services.object_storage,
                ),
            },
        ),
        split_tables_detector=domain_services.split_tables_detector,
        document_layout_repository=repositories.document_layout,
        raw_document_layout_repository=repositories.raw_document_layout,
        command_producer=command_producer,
        merge_tables_enabled=config.merge_tables_settings.enabled,
    )
    document_type_service: providers.Singleton[DocumentTypeService] = providers.Singleton(
        DocumentTypeService,
        document_type_repository=repositories.document_type,
        command_producer=command_producer,
    )

    semantic_layout_service = providers.Selector(
        providers.Callable(str.lower, providers.Callable(str, config.semantic_layout_enabled)),
        true=providers.Singleton(StubSemanticLayoutService),
        false=providers.Singleton(
            SemanticLayoutService,
            semantic_parsing_proxy=external_services.semantic_parsing,
        ),
    )

    parsing_service: providers.Singleton[ParsingService] = providers.Singleton(
        ParsingService,
        document_proxy=external_services.document,
        document_type_repository=repositories.document_type,
        command_producer=command_producer,
        dl_service=document_layout_service,
        tl_service=tabular_layout_service,
        semantic_layout_service=semantic_layout_service,
        default_ocr_engine=config.default_ocr_engine,
    )

    semantic_layout_application_v2 = providers.Selector(
        providers.Callable(str.lower, providers.Callable(str, config.semantic_layout_enabled)),
        true=providers.Singleton(StubSemanticLayoutApplicationV2),
        false=providers.Singleton(SemanticLayoutApplicationV2, command_producer=command_producer),
    )

    parsing_service_v2: providers.Singleton[ParsingServiceV2] = providers.Singleton(
        ParsingServiceV2,
        storage=external_services.object_storage,
        document_type_repository=repositories.document_type,
        command_producer=command_producer,
        dl_service=document_layout_service_v2,
        tl_service=tabular_layout_service_v2,
        semantic_service=semantic_layout_application_v2,
        default_ocr_engine=config.default_ocr_engine,
    )


class Containers(containers.DeclarativeContainer):
    config = providers.Configuration()
    current_user_tenant = providers.Callable(lambda: user.get()["organisation"])
    messaging_driver_settings = providers.Dependency(instance_of=object)

    datasources: providers.Container[Datasources] = providers.Container(
        Datasources,
        config=config.database,
    )

    external_services: providers.Container[ExternalServices] = providers.Container(
        ExternalServices,
        config=config,
    )

    repositories: providers.Container[Repositories] = providers.Container(
        Repositories,
        config=config,
        datasources=datasources,
        external_services=external_services,
    )

    core: providers.Container[Core] = providers.Container(Core, config=config)
    message_brokers: providers.Container[MessageBrokers] = providers.Container(
        MessageBrokers,
        config=config,
        messaging_driver_settings=messaging_driver_settings,
    )

    messaging: providers.Container[Messaging] = providers.Container(
        Messaging,
        config=config,
        message_brokers=message_brokers,
    )

    command_producer: providers.Singleton[CommandProducer] = providers.Singleton(
        CommandProducer,
        messaging.producer,
    )

    domain_event_publisher: providers.Singleton[DomainEventPublisher] = providers.Singleton(
        DomainEventPublisher,
        messaging.producer,
    )

    message_dispatcher: providers.Singleton[IMessageConsumer] = providers.Singleton(
        make_message_dispatcher,
        messaging.consumer,
        messaging.producer,
    )

    saga_command_producer: providers.Singleton[SagaCommandProducer] = providers.Singleton(
        SagaCommandProducer,
        command_producer,
    )

    saga_data_mapping: providers.Singleton[SagaDataMapping] = providers.Singleton(
        make_saga_data_mapping,
    )

    saga_manager_factory: providers.Singleton[SagaManagerFactory] = providers.Singleton(
        SagaManagerFactory,
        repositories.saga_instance,
        command_producer,
        messaging.consumer,
        saga_command_producer,
        saga_data_mapping,
    )

    saga_steps: providers.Container[SagaSteps] = providers.Container(
        SagaSteps,
        external_services=external_services,
    )

    sagas: providers.List = providers.List(
        providers.Singleton(PageParsingSaga, steps=saga_steps.page_parsing),
    )

    saga_instance_factory: providers.Singleton[SagaInstanceFactory] = providers.Singleton(
        SagaInstanceFactory,
        saga_manager_factory,
        sagas,
    )

    engines: providers.Container[Engines] = providers.Container(
        Engines,
        external_services=external_services,
        sagas=sagas,
        saga_instance_factory=saga_instance_factory,
    )

    domain_services: providers.Container[DomainServices] = providers.Container(
        DomainServices,
        config=config,
    )

    applications: providers.Container[Applications] = providers.Container(
        Applications,
        config=config,
        engines=engines,
        domain_services=domain_services,
        external_services=external_services,
        repositories=repositories,
        command_producer=command_producer,
        domain_event_publisher=domain_event_publisher,
    )
