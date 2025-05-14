import pytest
from unittest.mock import patch
from src.classifiers.zero_shot_classifier import zero_shot_classify

# Mock data for FILE_LABELS and ZERO_SHOT_SCORE
FILE_LABELS = ['label1', 'label2', 'label3']
ZERO_SHOT_SCORE = 0.5

# Test for successful classification (score above threshold)
def test_zero_shot_classify_success():
    mock_result = {
        'labels': ['label1', 'label2', 'label3'],
        'scores': [0.85, 0.1, 0.05]
    }

    with patch("src.classifiers.zero_shot_classifier.classifier", return_value=mock_result):
        label, score = zero_shot_classify("This is a test text")

    assert label == "label1"
    assert score == 0.85

# Test for score below threshold (should return 'unknown')
def test_zero_shot_classify_below_threshold():
    mock_result = {
        'labels': ['label2', 'label1', 'label3'],
        'scores': [0.4, 0.6, 0.1]
    }

    with patch("src.classifiers.zero_shot_classifier.classifier", return_value=mock_result):
        label, score = zero_shot_classify("This is another test text")

    assert label == "unknown"
    assert score == 0.4
