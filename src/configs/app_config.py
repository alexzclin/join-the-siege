ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'docx', 'xlsx'}

# Minimum confidence scores
FUZZY_SCORE = 90
ZERO_SHOT_SCORE = 0.9

# File categories and keywords for fuzzy string matching
FILE_LABELS = ['drivers_licence', 'bank_statement', 'invoice', 'unknown']
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
    ]
}
