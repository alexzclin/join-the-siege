import pytest
from io import BytesIO
from unittest.mock import patch, MagicMock
from werkzeug.datastructures import FileStorage

from src.classifiers.classifier import classify_file

@pytest.fixture
def fake_file():
    return FileStorage(
        stream=BytesIO(b"Fake PDF content that should extract text"),
        filename="test.pdf",
        content_type="application/pdf"
    )

@patch("src.classifiers.classifier.filetype.guess")
@patch("src.classifiers.classifier.extract_text")
@patch("src.classifiers.classifier.fuzzy_classify")
@patch("src.classifiers.classifier.sbert_classify")
@patch("src.classifiers.classifier.zero_shot_classify")
def test_classify_file_fuzzy_success(mock_zero_shot, mock_sbert, mock_fuzzy, mock_extract_text, mock_guess, fake_file):
    mock_guess.return_value = MagicMock(mime="application/pdf")
    mock_extract_text.return_value = "Some extracted text"
    mock_fuzzy.return_value = ("invoice", 0.9)  # Above FUZZY_SCORE
    mock_sbert.return_value = ("other", 0.0)
    mock_zero_shot.return_value = ("other", 0.0)

    result = classify_file(fake_file)

    assert result["label"] == "invoice"
    assert result["confidence"] == 0.9
    assert result["method"] == "content"

@patch("src.classifiers.classifier.filetype.guess", return_value=None)
def test_classify_file_undetectable_file_type(mock_guess, fake_file):
    result = classify_file(fake_file)
    assert result == {
        "label": "unknown",
        "confidence": 0.0,
        "method": "undetectable_file_type"
    }

@patch("src.classifiers.classifier.filetype.guess", return_value=MagicMock(mime="application/pdf"))
@patch("src.classifiers.classifier.extract_text", return_value="   ")
def test_classify_file_empty_text(mock_extract_text, mock_guess, fake_file):
    result = classify_file(fake_file)
    assert result == {
        "label": "unknown",
        "confidence": 0.0,
        "method": "empty_text"
    }

def test_classify_file_sbert_success(fake_file):
    with patch("src.classifiers.classifier.filetype.guess", return_value=MagicMock(mime="application/pdf")), \
         patch("src.classifiers.classifier.extract_text", return_value="some extracted text"), \
         patch("src.classifiers.classifier.fuzzy_classify", return_value=("fuzzy_label", 0.3)), \
         patch("src.classifiers.classifier.sbert_classify", return_value=("sbert_label", 0.8)), \
         patch("src.classifiers.classifier.zero_shot_classify") as mock_zero_shot:

        result = classify_file(fake_file)

    mock_zero_shot.assert_not_called()
    assert result == {
        "label": "sbert_label",
        "confidence": 0.8,
        "method": "sentence_bert"
    }

def test_classify_file_zero_shot_success(fake_file):
    with patch("src.classifiers.classifier.filetype.guess", return_value=MagicMock(mime="application/pdf")), \
         patch("src.classifiers.classifier.extract_text", return_value="some extracted text"), \
         patch("src.classifiers.classifier.fuzzy_classify", return_value=("fuzzy_label", 0.3)), \
         patch("src.classifiers.classifier.sbert_classify", return_value=("sbert_label", 0.3)), \
         patch("src.classifiers.classifier.zero_shot_classify", return_value=("zs_label", 0.85)):

        result = classify_file(fake_file)

    assert result == {
        "label": "zs_label",
        "confidence": 0.85,
        "method": "zero_shot"
    }

def test_classify_file_uncategorizable(fake_file):
    with patch("src.classifiers.classifier.filetype.guess", return_value=MagicMock(mime="application/pdf")), \
         patch("src.classifiers.classifier.extract_text", return_value="some extracted text"), \
         patch("src.classifiers.classifier.fuzzy_classify", return_value=("fuzzy_label", 0.2)), \
         patch("src.classifiers.classifier.sbert_classify", return_value=("sbert_label", 0.3)), \
         patch("src.classifiers.classifier.zero_shot_classify", return_value=("zs_label", 0.3)):

        result = classify_file(fake_file)

    assert result == {
        "label": "unknown",
        "confidence": 0.0,
        "method": "uncategorizable"
    }
