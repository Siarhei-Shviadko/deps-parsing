from google.cloud.documentai import Document as DocAIDocument

__all__ = [
    "DocAIDocument",
    "DocAILayout",
    "DocAIParagraph",
    "DocAILine",
    "DocAIWord",
    "DocAIKeyValuePair",
    "DocAITable",
    "DocAICell",
    "DocAIRow",
    "DocAIPage",
]

DocAIPage = DocAIDocument.Page
DocAILayout = DocAIDocument.Page.Layout
DocAIParagraph = DocAIDocument.Page.Paragraph
DocAILine = DocAIDocument.Page.Line
DocAIWord = DocAIDocument.Page.Token
DocAIKeyValuePair = DocAIDocument.Page.FormField
DocAITable = DocAIDocument.Page.Table
DocAICell = DocAITable.TableCell
DocAIRow = DocAITable.TableRow
