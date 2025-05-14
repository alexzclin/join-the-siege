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
        'driver\'s license', 'drivers licence', 'driver license',
        'id card', 'identity card', 'identification',
        'license number', 'dl number', 'class', 'expiry date', 'issued', 'endorsements'
    ],
    'bank_statement': [
        'bank statement', 'statement of account', 'account summary',
        'transaction history', 'account activity', 'account balance',
        'deposit', 'withdrawal', 'direct deposit', 'statement period',
        'available balance', 'opening balance', 'closing balance'
    ],
    'invoice': [
        'invoice', 'receipt', 'bill', 'purchase order', 'order number',
        'amount due', 'subtotal', 'total amount', 'due date',
        'invoice date', 'billing address', 'payment terms', 'item description'
    ],
    'health_insurance_card': [
        'health insurance card', 'insurance card', 'health plan card', 'medical insurance card',
        'policy number', 'member id', 'group number', 'plan type', 'coverage start date',
        'coverage end date', 'issuer', 'insured', 'benefits', 'medical plan', 'health coverage',
        'coverage', 'insurance provider', 'policyholder', 'premium', 'insured name', 'healthcare provider'
    ]
}

# BERT configurations
SBERT_MODEL = "all-MiniLM-L6-v2"
CLASSIFIER_PATH = "src/document_classifier.pkl"
