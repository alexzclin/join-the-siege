import pytest
from unittest.mock import patch, MagicMock
from src.classifiers.sbert_classifier import sbert_classify


@pytest.fixture(autouse=True)
def reset_model_cache():
    # Reset the global _clf and _embedder before each test
    import src.classifiers.sbert_classifier as sbert_mod
    sbert_mod._clf = None
    sbert_mod._embedder = None


def test_sbert_classify_success():
    mock_clf = MagicMock()
    mock_embedder = MagicMock()

    mock_clf.predict.return_value = ["label1"]
    mock_clf.predict_proba.return_value = [[0.2, 0.8]]
    mock_embedder.encode.return_value = [[0.1, 0.2, 0.3]]

    with patch("src.classifiers.sbert_classifier.os.path.exists", return_value=True), \
         patch("src.classifiers.sbert_classifier.joblib.load", return_value=mock_clf), \
         patch("src.classifiers.sbert_classifier.SentenceTransformer", return_value=mock_embedder):

        label, score = sbert_classify("This is a test sentence")

    assert label == "label1"
    assert score == 0.8
    mock_clf.predict.assert_called_once()
    mock_embedder.encode.assert_called_once()

def test_sbert_classify_partial_missing_embedder():
    mock_clf = MagicMock()

    with patch("src.classifiers.sbert_classifier._load_models", return_value=(mock_clf, None)), \
         patch("src.classifiers.sbert_classifier.logger.warning") as mock_logger:

        label, score = sbert_classify("Embedding should fail")

    assert label == "unknown"
    assert score == 0.0
    mock_logger.assert_called_once()
