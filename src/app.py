from flask import Flask, request, jsonify, g
from src.classifiers.classifier import classify_file
from src.configs.logging_config import setup_logging
import uuid
from werkzeug.exceptions import RequestEntityTooLarge
from src.utils.file_utils import allowed_file
from src.configs.app_config import MAX_CONTENT_LENGTH

setup_logging()
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

@app.before_request
def assign_request_id():
    g.request_id = request.headers.get('X-Request-ID', str(uuid.uuid4()))

@app.route('/classify_file', methods=['POST'])
def classify_file_route():

    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": f"File type not allowed"}), 400

    file_class = classify_file(file)
    return jsonify({"file_class": file_class}), 200

@app.errorhandler(RequestEntityTooLarge)
def handle_file_too_large(e):
    return jsonify({"error": "File is too large"}), 413


if __name__ == '__main__':
    app.run(debug=True)
