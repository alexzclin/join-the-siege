import pytest
from unittest.mock import patch
from src.classifiers.fuzzy_classifier import fuzzy_classify
from src.configs.app_config import MATCH_TERMS

# Test configuration for MATCH_TERMS
MATCH_TERMS = {
    "label1": ["term1", "term2"],
    "label2": ["term3", "term4"],
    "label3": ["term5"]
}

@pytest.mark.parametrize(
    "text, expected_label, expected_score",
    [
        ("This is a term1", "label1", 1.0),  # matches term1
        ("This is a term3", "label2", 1.0),  # matches term3
        ("z", "unknown", 0.0),  # no match
        ("term1 and ter3", "label1", 1.0),  # term1 has the highest score
        ("term5 is here", "label3", 1.0),  # matches term5
    ]
)
def test_fuzzy_classify(text, expected_label, expected_score):
    with patch.dict("src.configs.app_config.MATCH_TERMS", MATCH_TERMS):
        label, score = fuzzy_classify(text)
        assert label == expected_label
        assert score == expected_score
