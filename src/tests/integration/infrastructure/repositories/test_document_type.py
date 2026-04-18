def test_save_document_type__ok(document_type_repository, test_document_type):
    document_type_repository.save(test_document_type)
    restored_doc_type = document_type_repository.find_by_id_for_tenant(
        test_document_type.id(), test_document_type.tenant_id()
    )

    assert restored_doc_type == test_document_type


def test_save_same_document_type_twice__doc_type_updated(document_type_repository, test_document_type):
    document_type_repository.save(test_document_type)
    test_document_type.attach_command_channel("changed_cm")
    document_type_repository.save(test_document_type)
    updated_doc_type = document_type_repository.find_by_id_for_tenant(
        test_document_type.id(), test_document_type.tenant_id()
    )

    assert updated_doc_type.command_channel.name == "changed_cm"


def test_find_by_id_for_tenant__ok(test_saved_document_type, document_type_repository):
    saved_doc_type = document_type_repository.find_by_id_for_tenant(
        test_saved_document_type.id(), test_saved_document_type.tenant_id()
    )

    assert saved_doc_type == test_saved_document_type


def test_find_by_id_for_tenant__no_saved_doc_types__return_none(test_document_type, document_type_repository):
    saved_doc_type = document_type_repository.find_by_id_for_tenant(
        test_document_type.id(), test_document_type.tenant_id()
    )

    assert saved_doc_type is None


def test_save_all_document_types__ok(test_document_type, document_type_factory, document_type_repository):
    second_doc_type = document_type_factory()
    document_type_repository.save_all([test_document_type, second_doc_type])

    saved_doc_type_1 = document_type_repository.find_by_id(test_document_type.id())
    saved_doc_type_2 = document_type_repository.find_by_id(second_doc_type.id())
    assert saved_doc_type_1 and saved_doc_type_2


def test_save_all_document_types_twice__no_errors__all_saved(
    test_document_type, document_type_factory, document_type_repository
):
    second_doc_type = document_type_factory()
    document_type_repository.save_all([test_document_type])
    document_type_repository.save_all([second_doc_type])

    saved_doc_type_1 = document_type_repository.find_by_id(test_document_type.id())
    saved_doc_type_2 = document_type_repository.find_by_id(second_doc_type.id())
    assert saved_doc_type_1 and saved_doc_type_2


def test_save_all_document_types_twice__doc_types_updated(
    test_document_type, document_type_factory, document_type_repository
):
    second_doc_type = document_type_factory()
    document_type_repository.save_all([test_document_type, second_doc_type])
    test_document_type.attach_command_channel("new_command_channel_1")
    second_doc_type.attach_command_channel("new_command_channel_2")
    document_type_repository.save_all([test_document_type, second_doc_type])

    saved_doc_type_1 = document_type_repository.find_by_id(test_document_type.id())
    saved_doc_type_2 = document_type_repository.find_by_id(second_doc_type.id())
    assert saved_doc_type_1 and saved_doc_type_2
    assert saved_doc_type_1.command_channel.name == "new_command_channel_1"
    assert saved_doc_type_2.command_channel.name == "new_command_channel_2"


def test_find_by_id__ok(test_saved_document_type, document_type_repository):
    doc_type = document_type_repository.find_by_id(test_saved_document_type.id())

    assert doc_type == test_saved_document_type


def test_find_by_id__no_doc_type__no_errors(document_type_repository):
    doc_type = document_type_repository.find_by_id("fake_id")

    assert doc_type is None


def test_delete__ok(test_saved_document_type, document_type_repository):
    document_type_repository.delete(test_saved_document_type.id())

    assert document_type_repository.delete(test_saved_document_type.id()) is None


def test_delete__no_doc_type__no_errors(document_type_repository):
    assert document_type_repository.delete("fake") is None
