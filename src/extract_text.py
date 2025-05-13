import os
import logging
from werkzeug.datastructures import FileStorage
from src.extractors.registry import MIME_EXTRACTOR_REGISTRY, EXTENSION_EXTRACTOR_REGISTRY

logger = logging.getLogger(__name__)

def extract_text(file: FileStorage, type: str) -> str:
    extractor_type = MIME_EXTRACTOR_REGISTRY.get(type)

    # fall back to extension type for ambiguous mime
    if not extractor_type and type == "application/zip":
        ext = os.path.splitext(file.filename)[-1].lower()
        extractor_type = EXTENSION_EXTRACTOR_REGISTRY.get(ext)

    extractor = extractor_type()
    return extractor.extract(file)
