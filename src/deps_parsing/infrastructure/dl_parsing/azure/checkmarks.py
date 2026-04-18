from deps_parsing.domain.model import CheckmarkValue

__all__ = ["AzureCheckmarksMap"]


AzureCheckmarksMap = {
    ":unselected:": CheckmarkValue.UNCHECKED.value,
    ":selected:": CheckmarkValue.CHECKED.value,
}
