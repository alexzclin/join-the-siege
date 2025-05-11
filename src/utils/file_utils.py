from pypdf import PdfReader
from werkzeug.datastructures import FileStorage
import pytesseract
from PIL import Image
import docx2txt

def extract_text_from_pdf(file: FileStorage) -> str:
    try:
        reader = PdfReader(file)
        return " ".join([page.extract_text() for page in reader.pages])
    except Exception as e:
        print(f"Error reading {file}: {e}")
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