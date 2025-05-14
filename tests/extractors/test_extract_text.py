import pytest
from io import BytesIO
from unittest.mock import patch, MagicMock
from werkzeug.datastructures import FileStorage

from src.extractors.registry import MIME_EXTRACTOR_REGISTRY, EXTENSION_EXTRACTOR_REGISTRY
from src.extractors.extract_text import extract_text

@pytest.fixture
def fake_xlsx_file():
    return FileStorage(
        stream=BytesIO(b"fake xlsx content"),
        filename="test.xlsx",
        content_type="application/zip"
    )

def test_extract_text_with_mime(fake_xlsx_file):
    extractor_mock = MagicMock()
    extractor_mock.extract.return_value = "Extracted content"
    
    with patch.dict(MIME_EXTRACTOR_REGISTRY, {"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": lambda: extractor_mock}):
        result = extract_text(fake_xlsx_file, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    
    extractor_mock.extract.assert_called_once_with(fake_xlsx_file)
    assert result == "Extracted content"


def test_extract_text_with_zip_and_extension(fake_xlsx_file):
    extractor_mock = MagicMock()
    extractor_mock.extract.return_value = "Extracted from ZIP"
    
    # Fall back to file extension for 'application/zip' (mimicking zip file logic)
    with patch.dict(EXTENSION_EXTRACTOR_REGISTRY, {".xlsx": lambda: extractor_mock}):
        result = extract_text(fake_xlsx_file, "application/zip")
    
    extractor_mock.extract.assert_called_once_with(fake_xlsx_file)
    assert result == "Extracted from ZIP"
