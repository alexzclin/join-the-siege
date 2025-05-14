import docx2txt
import logging
from werkzeug.datastructures import FileStorage
from .base import BaseExtractor

logger = logging.getLogger(__name__)

class DocxExtractor(BaseExtractor):
    def extract(self, file: FileStorage) -> str:
        try:
            return docx2txt.process(file)
        except Exception as e:
            logger.error(f"Error extracting DOCX: {e}", exc_info=True)
            return ""
