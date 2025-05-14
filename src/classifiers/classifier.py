from werkzeug.datastructures import FileStorage
from typing import Dict
from transformers import pipeline
import filetype
import logging
from ..extractors.extract_text import extract_text
from src.configs.app_config import FUZZY_SCORE, ZERO_SHOT_SCORE, SBERT_SCORE
from src.classifiers.fuzzy_classify import fuzzy_classify
from src.classifiers.zero_shot_classify import zero_shot_classify
from src.classifiers.sbert_classify import sbert_classify

logger = logging.getLogger(__name__)

def classify_file(file: FileStorage) -> Dict:
    logger.info(f"Starting classification of file: {file.filename}")

    # Detect type from first 261 bytes as recommended by filetype
    header = file.read(261)
    file.seek(0)  # Reset the pointer
    type = filetype.guess(header)
    if type is None:
        logger.info(f"Filetype could not be determined for the file: {file.fileName}")
        return {
            'label': 'unknown',
            'confidence': 0.0,
            'method': 'undetectable_file_type'
        }
    
    extracted_text = extract_text(file, type.mime)
    if not extracted_text.strip():
        logger.info(f"Text could not be extracted from the file: {file.fileName}")
        return {
            'label': 'unknown',
            'confidence': 0.0,
            'method': 'empty_text'
        }

    fuzzy_label, fuzzy_score = fuzzy_classify(extracted_text)
    if fuzzy_score >= FUZZY_SCORE:
        logger.info(f"File {file.filename} classified using fuzzy string classification with label {fuzzy_label} and confidence {fuzzy_score}")
        return {
            'label': fuzzy_label,
            'confidence': fuzzy_score,
            'method': 'content'
        }
    
    sbert_label, sbert_score = sbert_classify(extracted_text)
    if sbert_score >= SBERT_SCORE:
        logger.info(f"File {file.filename} classified using Sentence-BERT classification with label {sbert_label} and confidence {sbert_score}")
        return {
            'label': sbert_label,
            'confidence': sbert_score,
            'method': 'sentence_bert'
        }
    
    zero_shot_label, zero_shot_score = zero_shot_classify(extracted_text)
    if zero_shot_score >= ZERO_SHOT_SCORE:
        logger.info(f"File {file.filename} classified using zero-shot classification with label {zero_shot_label} and confidence {zero_shot_score}")
        return {
            'label': zero_shot_label,
            'confidence': zero_shot_score,
            'method': 'zero_shot'
        }
    
    logger.info(f"File {file.filename} could not be classified with sufficient confidence")
    return {'label': 'unknown', 'confidence': 0.0, 'method': 'uncategorizable'}
