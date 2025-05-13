from rapidfuzz import fuzz
from typing import Tuple
from src.configs.app_config import MATCH_TERMS
import logging

logger = logging.getLogger(__name__)

def fuzzy_classify(text: str) -> Tuple[str, float]:
    best_category, best_score = 'unknown', 0
    for category, terms in MATCH_TERMS.items():
        for term in terms:
            score = fuzz.partial_ratio(text.lower(), term.lower())
            if score > best_score:
                best_category, best_score = category, score
    logger.info(f"Heuristic classification score: {best_score}")
    return best_category, round(best_score / 100.0, 2)
