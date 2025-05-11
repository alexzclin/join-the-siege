from werkzeug.datastructures import FileStorage
from typing import Dict, List, Tuple
from transformers import pipeline
from src.utils.file_utils import *
import os
import filetype
from rapidfuzz import fuzz

classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Minimum confidence scores
heuristic_classify_score = 90
zero_shot_score = 0.9

# Categories and keywords
labels = ["drivers_licence", "bank_statement", "invoice", "unknown"]
match_terms = {
    'drivers_licence': ['license', 'id card', 'identification', 'driver'],
    'bank_statement': ['bank', 'statement', 'account history', 'direct deposit', 'account holder'],
    'invoice': ['invoice', 'receipt', 'bill']
}

def classify_file(file: FileStorage) -> Dict:
    # Read a small chunk of the file to detect type
    header = file.read(261)  # filetype docs recommend reading first 261 bytes
    file.seek(0)  # Reset the pointer so downstream code can read the whole file

    kind = filetype.guess(header)

    if kind is None:
        return {
            'category': 'unknown',
            'confidence': 0.0,
            'method': 'undetectable_file_type'
        }

    mime = kind.mime
    if mime == 'application/pdf':
        extracted_text = extract_text_from_pdf(file)
    elif mime in ('image/jpeg', 'image/png'):
        extracted_text = extract_text_from_image(file)
    else:
        return {
            'category': 'unknown',
            'confidence': 0.0,
            'method': f'unsupported_file_type:{mime}'
        }

    if not extracted_text.strip():
        return {
            'category': 'unknown',
            'confidence': 0.0,
            'method': 'empty_text'
        }

    content_guess, content_score = heuristic_classify(extracted_text)
    if content_score >= heuristic_classify_score / 100:
        return {'category': content_guess, 'confidence': content_score, 'method': 'content'}

    model_guess, model_score = zero_shot_classify(extracted_text)
    return {'category': model_guess, 'confidence': model_score, 'method': 'model'}

def heuristic_classify(text: str) -> Tuple[str, float]:
    best_category, best_score = 'unknown', 0
    for category, terms in match_terms.items():
        for term in terms:
            score = fuzz.partial_ratio(text.lower(), term.lower())
            if score > best_score:
                best_category, best_score = category, score
    return best_category, best_score / 100.0

def zero_shot_classify(text: str) -> Tuple[str, float]:
    result = classifier(text, candidate_labels=labels)
    label, score = result['labels'][0], result['scores'][0]
    return (label, score) if score >= zero_shot_score else ('unknown', score)