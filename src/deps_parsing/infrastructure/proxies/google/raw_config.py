from typing import TypedDict

__all__ = ["RawDocAIConfig"]


class RawDocAIConfig(TypedDict):
    project_id: str
    location: str

    form_recognition_processor_id: str

    account_info_json: str

    idp_token_url: str
    idp_client_id: str
    idp_client_secret: str
