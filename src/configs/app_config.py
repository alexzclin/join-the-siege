ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'docx', 'xlsx'}
MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10 MB file size limit

# Minimum confidence scores
FUZZY_SCORE = 0.9
SBERT_SCORE = 0.8
ZERO_SHOT_SCORE = 0.8

# File categories and keywords for fuzzy string matching
# Add similar entries here when expanding to new industries
FILE_LABELS = ['drivers_licence', 'bank_statement', 'invoice', 'health_insurance_card' 'unknown']
MATCH_TERMS = {
    'drivers_licence': [
        "driver's license", "drivers licence", "driver license",
        "dl number", "license number", "licence no", "class", "expiry date",
        "date of birth", "dob", "issued on", "issuing state", "endorsements",
        "restrictions", "state of issue", "sex", "eye color", "height",
        "organ donor", "identification card", "id card", "identity card"
    ],
    'bank_statement': [
        "bank statement", "statement of account", "account summary",
        "account activity", "transaction history", "deposits", "withdrawals",
        "direct deposit", "available balance", "account balance",
        "statement date", "opening balance", "closing balance",
        "account holder", "account number", "routing number",
        "interest earned", "monthly summary", "financial institution"
    ],
    'invoice': [
        "invoice", "invoice number", "receipt", "sales receipt", "bill",
        "purchase order", "po number", "order number", "invoice date",
        "billing address", "shipping address", "amount due", "due date",
        "item", "item description", "quantity", "unit price", "subtotal",
        "tax", "total", "total amount", "payment terms", "paid", "balance due"
    ],
    'health_insurance_card': [
        'health insurance card', 'insurance card', 'health plan card', 'medical insurance card',
        'policy number', 'member id', 'group number', 'plan type', 'coverage start date',
        'coverage end date', 'issuer', 'insured', 'benefits', 'medical plan', 'health coverage',
        'coverage', 'insurance provider', 'policyholder', 'premium', 'insured name', 'healthcare provider'
    ]
}

# model configurations
SBERT_MODEL = "all-MiniLM-L6-v2"
CLASSIFIER_PATH = "src/document_classifier.pkl"
ZERO_SHOT_MODEL = "facebook/bart-large-mnli"
