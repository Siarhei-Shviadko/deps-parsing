def test_attach_parsing_plugin__doc_type_exists__ok(
    document_type_repository_mock, document_type_service, document_type_factory
):
    doc_type = document_type_factory(command_channel=None)
    document_type_repository_mock.find_by_id.return_value = doc_type
    document_type_repository_mock.save.return_value = None

    document_type_service.attach_parsing_plugin(doc_type.id(), "parsing_command_channel")

    document_type_repository_mock.save.assert_called_with(doc_type)
    assert doc_type.command_channel.name == "parsing_command_channel"


def test_attach_parsing_plugin__doc_type_not_exists__ok(document_type_repository_mock, document_type_service):
    document_type_repository_mock.find_by_id.return_value = None
    document_type_repository_mock.save.return_value = "Catch"
    document_type_service.attach_parsing_plugin("my_id", "parsing_command_channel")

    document_type_repository_mock.save.assert_not_called()
