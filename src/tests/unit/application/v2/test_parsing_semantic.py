from uuid import uuid4

from deps_parsing.application.semantic_parsing_type import SemanticParsingType


def test_perform_parsing__semantic_engine__routes_to_semantic_service(
    parsing_service_v2,
    semantic_layout_application_v2_mock,
    tenant_id,
):
    entity_id = uuid4().hex
    file_path = f"{entity_id}.docx"

    parsing_service_v2.perform_parsing(
        entity_id=entity_id,
        tenant_id=tenant_id,
        file_path=file_path,
        engine="LLAMAINDEX",
    )

    semantic_layout_application_v2_mock.parse.assert_called_once()
    call_kwargs = semantic_layout_application_v2_mock.parse.call_args.kwargs
    assert call_kwargs["entity_id"] == entity_id
    assert call_kwargs["tenant_id"] == tenant_id
    assert call_kwargs["parsing_type"] == SemanticParsingType.LLAMAINDEX
    parsing_service_v2._dl_service.parse.assert_not_called()


def test_perform_parsing__semantic_engine__forwards_routing_info(
    parsing_service_v2,
    semantic_layout_application_v2_mock,
    tenant_id,
):
    entity_id = uuid4().hex
    routing_info = {"saga-id": "saga-123"}

    parsing_service_v2.perform_parsing(
        entity_id=entity_id,
        tenant_id=tenant_id,
        file_path=f"{entity_id}.pdf",
        engine="LLAMAINDEX",
        routing_info=routing_info,
    )

    call_kwargs = semantic_layout_application_v2_mock.parse.call_args.kwargs
    assert call_kwargs["routing_info"] == routing_info


def test_perform_parsing__ocr_engine_on_docx__routes_to_dl_service(
    parsing_service_v2,
    semantic_layout_application_v2_mock,
    tenant_id,
):
    entity_id = uuid4().hex

    parsing_service_v2.perform_parsing(
        entity_id=entity_id,
        tenant_id=tenant_id,
        file_path=f"{entity_id}.docx",
        engine="TESSERACT",
    )

    parsing_service_v2._dl_service.parse.assert_called_once()
    semantic_layout_application_v2_mock.parse.assert_not_called()


def test_perform_parsing__no_engine_docx__falls_back_to_dl_service(
    parsing_service_v2,
    semantic_layout_application_v2_mock,
    tenant_id,
):
    entity_id = uuid4().hex

    parsing_service_v2.perform_parsing(
        entity_id=entity_id,
        tenant_id=tenant_id,
        file_path=f"{entity_id}.docx",
    )

    parsing_service_v2._dl_service.parse.assert_called_once()
    semantic_layout_application_v2_mock.parse.assert_not_called()


def test_perform_parsing__semantic_engine_on_xlsx__routes_to_semantic_service(
    parsing_service_v2,
    semantic_layout_application_v2_mock,
    tenant_id,
):
    entity_id = uuid4().hex

    parsing_service_v2.perform_parsing(
        entity_id=entity_id,
        tenant_id=tenant_id,
        file_path=f"{entity_id}.xlsx",
        engine="LLAMAINDEX",
    )

    semantic_layout_application_v2_mock.parse.assert_called_once()
    parsing_service_v2._tl_service.parse.assert_not_called()
