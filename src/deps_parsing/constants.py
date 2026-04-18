PROJECT_NAME = "parsing"
DESCRIPTION = "Parsing service for storing standardized structure"
V1_PREFIX = "/v1"
V2_PREFIX = "/v2"
BASE_API_PREFIX = "/api/parsing"
V1_API_PREFIX = BASE_API_PREFIX + V1_PREFIX
V2_API_PREFIX = BASE_API_PREFIX + V2_PREFIX
SWAGGER_DOC_URL = "/docs"

DOCUMENTS_EXCHANGER = "Documents"
FILE_EXCHANGER = "File"
DOCUMENT_TYPE_EXCHANGER = "DocumentType"
REFERENCE_LAYOUT_EXCHANGER = "ReferenceLayout"
TABULAR_LAYOUT_EXCHANGER = "TabularLayout"

EVENTS_QUEUE = "parsing-events"
COMMANDS_QUEUE = "parsing-commands"

SERVICE_CHANNEL = "ParsingService"
COMMANDS_CHANNEL = "ParsingCommands"
COMMANDS_REPLIES_CHANNEL = "ParsingCommandsReplies"

DOCUMENT_LAYOUT_FOLDER = "document_layout"
