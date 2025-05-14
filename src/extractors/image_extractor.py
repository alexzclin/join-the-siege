import pytesseract
from PIL import Image, ImageOps
import logging
from werkzeug.datastructures import FileStorage
from .base import BaseExtractor

logger = logging.getLogger(__name__)

class ImageExtractor(BaseExtractor):
    def extract(self, file: FileStorage) -> str:
        try:
            image = Image.open(file)
            return pytesseract.image_to_string(image)
        except Exception as e:
            logger.error(f"Error extracting from image: {e}", exc_info=True)
            return ""
