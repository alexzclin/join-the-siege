import os
import joblib
from sentence_transformers import SentenceTransformer
from typing import Tuple
from src.configs.app_config import SBERT_MODEL, CLASSIFIER_PATH
import logging

os.environ["TOKENIZERS_PARALLELISM"] = "false"

logger = logging.getLogger(__name__)

# Cache models for reuse
_clf = None
_embedder = None

def _load_models():
    global _clf, _embedder
    if _clf is None and os.path.exists(CLASSIFIER_PATH):
        _clf = joblib.load(CLASSIFIER_PATH)
    if _embedder is None:
        _embedder = SentenceTransformer(SBERT_MODEL)
    return _clf, _embedder

def sbert_classify(text: str) -> Tuple[str, float]:
    clf, embedder = _load_models()
    if clf is None or embedder is None:
        logger.warning(f"Trained classifier is not found at path {CLASSIFIER_PATH}")
        return "unknown", 0.0
    
    embedding = embedder.encode([text])[0]
    label = clf.predict([embedding])[0]
    score = max(clf.predict_proba([embedding])[0])
    logger.info(f"Sentence-BERT classification label: {label}, score: {score}")
    return label, round(score, 2)
