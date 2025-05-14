import pytest
from unittest.mock import patch, MagicMock
from werkzeug.datastructures import FileStorage
from src.extractors.image_extractor import ImageExtractor

# Sample Image file fixture
@pytest.fixture
def fake_image_file():
    # Create a fake image as FileStorage input
    return FileStorage(
        stream=b"fake image content",  # Fake binary content, this would be replaced with real image content in real scenarios
        filename="test.png",
        content_type="image/png"
    )

# Test successful extraction (OCR)
def test_image_extractor_success(fake_image_file):
    extractor = ImageExtractor()

    mock_image = MagicMock(name="Image")
    mock_ocr_result = "Extracted text from image"

    with patch("src.extractors.image_extractor.Image.open", return_value=mock_image) as mock_open, \
         patch("src.extractors.image_extractor.pytesseract.image_to_string", return_value=mock_ocr_result) as mock_ocr:
        
        result = extractor.extract(fake_image_file)

    mock_open.assert_called_once_with(fake_image_file)
    mock_ocr.assert_called_once_with(mock_image)
    assert result == mock_ocr_result

# Test extraction failure (e.g., corrupt image)
def test_image_extractor_failure(fake_image_file):
    extractor = ImageExtractor()

    # Simulate a failure when opening the image (e.g., corrupt image)
    with patch("src.extractors.image_extractor.Image.open", side_effect=Exception("corrupt image")) as mock_open:
        result = extractor.extract(fake_image_file)

    mock_open.assert_called_once_with(fake_image_file)
    assert result == "" 

# Test logging on failure
def test_image_extractor_logging_on_failure(fake_image_file):
    extractor = ImageExtractor()

    with patch("src.extractors.image_extractor.Image.open", side_effect=Exception("corrupt image")) as mock_open, \
         patch("src.extractors.image_extractor.logger.error") as mock_logger:

        result = extractor.extract(fake_image_file)

    mock_logger.assert_called_once_with("Error extracting from image: corrupt image", exc_info=True)
    assert result == "" 
