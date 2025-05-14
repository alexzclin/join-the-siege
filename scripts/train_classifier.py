import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
from sentence_transformers import SentenceTransformer

# CONFIG
CSV_PATH = "data/synthetic_data.csv"
MODEL_PATH = "src/document_classifier.pkl"
SBERT_MODEL_NAME = "all-MiniLM-L6-v2"

# Load synthetic dataset
df = pd.read_csv(CSV_PATH)
texts = df["text"].tolist()
labels = df["label"].tolist()

# Load Sentence-BERT model
embedder = SentenceTransformer(SBERT_MODEL_NAME)

# Encode texts to embeddings
print("Encoding documents...")
embeddings = embedder.encode(texts, show_progress_bar=True)

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(embeddings, labels, test_size=0.2, random_state=42)

# Train classifier
print("Training Logistic Regression classifier...")
clf = LogisticRegression(max_iter=1000)
clf.fit(X_train, y_train)

# Evaluate
y_pred = clf.predict(X_test)
print("Classification report:")
print(classification_report(y_test, y_pred))

# Save model
joblib.dump(clf, MODEL_PATH)
print(f"Saved model to {MODEL_PATH}")
