import pytest
from io import BytesIO
from unittest.mock import patch, MagicMock
from werkzeug.datastructures import FileStorage

from src.extractors.xlsx_extractor import XlsxExtractor


@pytest.fixture
def fake_xlsx_file():
    return FileStorage(
        stream=BytesIO(b"fake xlsx content"),
        filename="test.xlsx",
        content_type="application/zip"
    )


def test_xlsx_extractor_success(fake_xlsx_file):
    extractor = XlsxExtractor()

    mock_xlsx = MagicMock()
    mock_xlsx.sheet_names = ['Sheet1', 'Sheet2']

    df1 = MagicMock()
    df1.fillna.return_value.to_string.return_value = "A B\n1 2"
    
    df2 = MagicMock()
    df2.fillna.return_value.to_string.return_value = "X Y\n3 4"

    with patch("src.extractors.xlsx_extractor.pd.ExcelFile", return_value=mock_xlsx), \
         patch("src.extractors.xlsx_extractor.pd.read_excel", side_effect=[df1, df2]):

        result = extractor.extract(fake_xlsx_file)

    expected = (
        "\n\n--- Sheet: Sheet1 ---\nA B\n1 2"
        "\n\n--- Sheet: Sheet2 ---\nX Y\n3 4"
    )
    assert result == expected


def test_xlsx_extractor_empty_sheet_list(fake_xlsx_file):
    extractor = XlsxExtractor()

    mock_xlsx = MagicMock()
    mock_xlsx.sheet_names = []

    with patch("src.extractors.xlsx_extractor.pd.ExcelFile", return_value=mock_xlsx):
        result = extractor.extract(fake_xlsx_file)

    assert result == ""


def test_xlsx_extractor_failure(fake_xlsx_file):
    extractor = XlsxExtractor()

    with patch("src.extractors.xlsx_extractor.pd.ExcelFile", side_effect=Exception("Corrupted file")):
        result = extractor.extract(fake_xlsx_file)

    assert result == ""
