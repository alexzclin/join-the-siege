from rapidfuzz import fuzz
from typing import Tuple
from src.configs.app_config import MATCH_TERMS
import logging

logger = logging.getLogger(__name__)

def fuzzy_classify(text: str) -> Tuple[str, float]:
    best_label, best_score = 'unknown', 0
    for label, terms in MATCH_TERMS.items():
        for term in terms:
            score = fuzz.partial_ratio(text.lower(), term.lower())
            if score > best_score:
                best_label, best_score = label, score
    logger.info(f"Fuzzy classification label: {best_label}, score: {best_score}")
    return best_label, round(best_score / 100.0, 2)
