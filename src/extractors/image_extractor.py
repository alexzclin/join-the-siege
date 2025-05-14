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
            image = self._preprocess_image_for_ocr(image)
            return pytesseract.image_to_string(image)
        except Exception as e:
            logger.error(f"Error extracting from image: {e}", exc_info=True)
            return ""
        
    def _preprocess_image_for_ocr(image: Image.Image) -> Image.Image:
        image = image.convert('L')
        image = ImageOps.autocontrast(image)
        image = image.point(lambda x: 0 if x < 140 else 255, '1')
        image = image.resize((image.width * 2, image.height * 2), Image.LANCZOS)
        return image
