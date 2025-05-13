from typing import Dict, Type
from .base import BaseExtractor
from .pdf_extractor import PDFExtractor
from .docx_extractor import DocxExtractor
from .image_extractor import ImageExtractor
from .xlsx_extractor import XlsxExtractor

MIME_EXTRACTOR_REGISTRY: Dict[str, Type[BaseExtractor]] = {
    "application/pdf": PDFExtractor,
    "image/jpeg": ImageExtractor,
    "image/png": ImageExtractor,
}

EXTENSION_EXTRACTOR_REGISTRY: Dict[str, Type[BaseExtractor]] = {
    ".docx": DocxExtractor,
    ".xlsx": XlsxExtractor,
}
