import logging
from typing import Tuple
from transformers import pipeline
from src.configs.app_config import FILE_LABELS, ZERO_SHOT_SCORE, ZERO_SHOT_MODEL

logger = logging.getLogger(__name__)
classifier = pipeline('zero-shot-classification', model=ZERO_SHOT_MODEL)

def zero_shot_classify(text: str) -> Tuple[str, float]:
    result = classifier(text, candidate_labels=FILE_LABELS)
    label, score = result['labels'][0], result['scores'][0]
    logger.info(f"Zero-shot classification label: {label}, score: {score}")
    score = round(score, 2)
    return (label, score) if score >= ZERO_SHOT_SCORE else ('unknown', score)
