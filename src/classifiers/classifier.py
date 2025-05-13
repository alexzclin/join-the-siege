from werkzeug.datastructures import FileStorage
from typing import Dict
from transformers import pipeline
import filetype
import logging
from ..extract_text import extract_text
from src.configs.app_config import FUZZY_SCORE
from src.classifiers.fuzzy_classify import fuzzy_classify
from src.classifiers.zero_shot_classify import zero_shot_classify

logger = logging.getLogger(__name__)

def classify_file(file: FileStorage) -> Dict:
    # Detect type from first 261 bytes as recommended by filetype
    header = file.read(261)
    file.seek(0)  # Reset the pointer
    type = filetype.guess(header)
    if type is None:
        logger.info(f"Filetype could not be determined for the file: {file.fileName}")
        return {
            'category': 'unknown',
            'confidence': 0.0,
            'method': 'undetectable_file_type'
        }
    
    extracted_text = extract_text(file, type.mime)
    if not extracted_text.strip():
        logger.info(f"Text could not be extracted from the file: {file.fileName}")
        return {
            'category': 'unknown',
            'confidence': 0.0,
            'method': 'empty_text'
        }

    content_guess, content_score = fuzzy_classify(extracted_text)
    if content_score >= FUZZY_SCORE / 100:
        return {'category': content_guess, 'confidence': content_score, 'method': 'content'}

    model_guess, model_score = zero_shot_classify(extracted_text)
    return {'category': model_guess, 'confidence': model_score, 'method': 'model'}
