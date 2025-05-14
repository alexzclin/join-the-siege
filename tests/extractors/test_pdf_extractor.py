import pytest
from io import BytesIO
from unittest.mock import patch, MagicMock

from werkzeug.datastructures import FileStorage
from src.extractors.pdf_extractor import PDFExtractor


@pytest.fixture
def fake_pdf_file():
    return FileStorage(
        stream=BytesIO(b"%PDF-1.4 fake pdf content"),
        filename="test.pdf",
        content_type="application/pdf"
    )


def test_pdf_extractor_text_extraction(fake_pdf_file):
    extractor = PDFExtractor()

    # Mock PDF reader with a single page that has extractable text
    mock_page = MagicMock()
    mock_page.extract_text.return_value = "Some extracted text"
    mock_reader = MagicMock()
    mock_reader.pages = [mock_page]

    with patch("src.extractors.pdf_extractor.PdfReader", return_value=mock_reader):
        result = extractor.extract(fake_pdf_file)

    assert result == "Some extracted text"


def test_pdf_extractor_fallback_to_ocr(fake_pdf_file):
    extractor = PDFExtractor()

    # Mock PDF reader with no text
    mock_page = MagicMock()
    mock_page.extract_text.return_value = None
    mock_reader = MagicMock()
    mock_reader.pages = [mock_page]

    with patch("src.extractors.pdf_extractor.PdfReader", return_value=mock_reader), \
         patch.object(PDFExtractor, "_extract_with_ocr", return_value="OCR text") as mock_ocr:

        result = extractor.extract(fake_pdf_file)

    mock_ocr.assert_called_once()
    assert result == "OCR text"


def test_pdf_extractor_failure(fake_pdf_file):
    extractor = PDFExtractor()

    with patch("src.extractors.pdf_extractor.PdfReader", side_effect=Exception("broken PDF")):
        result = extractor.extract(fake_pdf_file)

    assert result == ""
