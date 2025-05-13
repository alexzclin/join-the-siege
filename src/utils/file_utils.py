from pypdf import PdfReader
from werkzeug.datastructures import FileStorage
import pytesseract
from PIL import Image
import docx2txt
from pdf2image import convert_from_bytes
import logging
import pandas as pd
from io import BytesIO

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_text_from_pdf(file: FileStorage) -> str:
    try:
        reader = PdfReader(file)
        extracted_text = " ".join([page.extract_text() for page in reader.pages])

        # Fallback to OCR if no text found
        if not extracted_text.strip():
            logger.info("Falling back to OCR to detect embedded images in the PDF")
            file.seek(0)
            extracted_text = extract_text_from_pdf_ocr(file)
        
        return extracted_text
    except Exception as e:
        print(f"Error reading {file}: {e}")
        return ""

def extract_text_from_pdf_ocr(file: FileStorage) -> str:
    try:
        images = convert_from_bytes(file.read())
        text = ""
        for image in images:
            text += pytesseract.image_to_string(image)
        return text
    except Exception as e:
        print(f"Error converting PDF to image for OCR: {e}")
        return ""

def extract_text_from_image(file: FileStorage) -> str:
    try:
        image = Image.open(file)
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        print(f"Error processing image {file}: {e}")
        return ""

def extract_text_from_docx(file: FileStorage) -> str:
    try:
        return docx2txt.process(file)
    except Exception as e:
        print(f"Error processing Word document {file}: {e}")
        return ""

def extract_text_from_spreadsheet(file: FileStorage) -> str:
    try:
        filename = file.filename.lower()
        file.seek(0)
        content = BytesIO(file.read())

        if filename.endswith('.csv'):
            df = pd.read_csv(content, dtype=str)
            return df.fillna("").to_string(index=False)
        elif filename.endswith(('.xlsx')):
            xls = pd.ExcelFile(content)
            extracted_text = ""
            for sheet_name in xls.sheet_names:
                df = pd.read_excel(xls, sheet_name=sheet_name, dtype=str)
                extracted_text += f"\n\n--- Sheet: {sheet_name} ---\n"
                extracted_text += df.fillna("").to_string(index=False)
            return extracted_text
        else:
            return "Unsupported file type for spreadsheet parsing."
    except Exception as e:
        print(f"Error processing spreadsheet {file.filename}: {e}")
        return ""

def extract_text_from_txt(file: FileStorage) -> str:
    try:
        file.seek(0)
        text = file.read().decode('utf-8', errors='ignore')
        return text
    except Exception as e:
        print(f"Error reading text file {file.filename}: {e}")
        return ""
