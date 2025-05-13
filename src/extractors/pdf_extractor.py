from pypdf import PdfReader
from pdf2image import convert_from_bytes
import pytesseract
import logging
from .base import BaseExtractor
from werkzeug.datastructures import FileStorage

logger = logging.getLogger(__name__)

class PDFExtractor(BaseExtractor):
    def extract(self, file: FileStorage) -> str:
        try:
            reader = PdfReader(file)
            text = " ".join(page.extract_text() or "" for page in reader.pages)
            if not text.strip():
                logger.info("Falling back to OCR for PDF")
                file.seek(0)
                text = self._extract_with_ocr(file)
            return text
        except Exception as e:
            logger.error(f"Error extracting PDF: {e}", exc_info=True)
            return ""

    def _extract_with_ocr(self, file: FileStorage) -> str:
        images = convert_from_bytes(file.read())
        return "".join(pytesseract.image_to_string(img) for img in images)
