import pandas as pd
from io import BytesIO
import logging
from werkzeug.datastructures import FileStorage
from .base import BaseExtractor

logger = logging.getLogger(__name__)

class XlsxExtractor(BaseExtractor):
    def extract(self, file: FileStorage) -> str:
        try:
            content = BytesIO(file.read())
            xlsx = pd.ExcelFile(content)
            extracted = ""
            for sheet_name in xlsx.sheet_names:
                df = pd.read_excel(xlsx, sheet_name=sheet_name, dtype=str)
                extracted += f"\n\n--- Sheet: {sheet_name} ---\n"
                extracted += df.fillna("").to_string(index=False)
            return extracted
        except Exception as e:
            logger.error(f"Error extracting XLSX: {e}", exc_info=True)
            return ""
