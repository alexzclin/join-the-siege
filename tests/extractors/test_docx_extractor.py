import pytest
from unittest.mock import patch, MagicMock
from werkzeug.datastructures import FileStorage
from io import BytesIO
from src.extractors.docx_extractor import DocxExtractor

@pytest.fixture
def fake_file():
    return FileStorage(stream=BytesIO(b"fake docx content"), filename="test.docx")

def test_docx_extractor_success(fake_file):
    extractor = DocxExtractor()

    with patch("src.extractors.docx_extractor.docx2txt.process", return_value="extracted text") as mock_process:
        result = extractor.extract(fake_file)

    mock_process.assert_called_once_with(fake_file)
    assert result == "extracted text"

def test_docx_extractor_failure(fake_file):
    extractor = DocxExtractor()

    with patch("src.extractors.docx_extractor.docx2txt.process", side_effect=Exception("parse error")) as mock_process:
        result = extractor.extract(fake_file)

    mock_process.assert_called_once_with(fake_file)
    assert result == ""
