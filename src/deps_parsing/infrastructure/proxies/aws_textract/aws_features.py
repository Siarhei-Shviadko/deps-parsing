from enum import Enum

__all__ = ["AWSFeature"]


class AWSFeature(Enum):
    TABLES = "TABLES"
    FORMS = "FORMS"
    QUERIES = "QUERIES"
    SIGNATURES = "SIGNATURES"
    LAYOUT = "LAYOUT"
