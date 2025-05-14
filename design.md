# Document Classifier Design

## Problem Statement
The default project implements a document classifier solution that relies on the string matching in the filename, which is a very specific and not extensible solution. This approach fails when file names are ambiguous or misleading, and it cannot generalize to new file types or industries accurately.

## Proposal
The solution will implement a robust and extensible document classifier API endpoint that relies on file content for accurate categorization. This approach improves reliability, reduces the impact of user error, and makes the system suitable for deployment in production environments across various industries.

### Requirements
1. Users should be able to upload different file types: pdf, png, jpg, docx, xlsx
1. Users should be able to receive accurate classification results for pre-defined labels based on the contents of the file
1. The classifier should be extensible to accommodate new industries and document types

### Assumptions
1. PDF files may contain scanned images or embedded text, which should be supported by OCR and parsing strategies.
1. When new industries or file types need to be supported, a manual onboarding process is acceptable. The process may involve adding support for new file extensions, adding new labels/match terms, and creating new synthetic data + fine-tuning the model again.
1. Large files are not supported and can be handled using input validation on file size
1. The following items are considered out of scope of the current design: 
    - User authentication/login and session management
    - Monitoring and observability features other than basic logging


## Design

To meet the requirement of content-based classification, we avoid trusting any user-provided metadata (e.g., filenames) for decision making. While the default implementation with filename-based classification is fast, it’s unreliable and does not scale well to handle more intricate document types.

For content extraction, we rely on a variety of Python libraries tailored for different file types. A fallback mechanism is implemented for PDF files to scan and extract embedded images using OCR (Optical Character Recognition). The extraction library used for each file type is as follows:
1. Images (.png, .jpg): Tesseract OCR
1. PDF (.pdf): PyPDF
1. Word Document (.docx): docx2txt
1. Excel Sheet (.xlsx): pandas

With text data extracted from input files, the solution takes a pipeline approach to attempt different classification mechanisms of increasing complexity. The more complex methods will yield higher accuracy at the cost of more expensive computation. If enough confidence is achieved from one mechanism, the classified label will be returned along with details like the confidence score and classification method. Here is the exact flow of the classification process:
1. Fuzzy String Matching: Initially, the system uses `RapidFuzz` to match the extracted text against a predefined set of document types, using similarity measures to categorize the document. This is the first step and works well for cases with exact or near-exact matches in content.
1. Sentence-BERT with Logistic Regression: If fuzzy string matching does not produce a satisfactory result, the system uses the `all-MiniLM-L6-v2` Sentence-BERT model. This model is fine-tuned on synthetic training data specific to the target domain, combined with logistic regression to classify the extracted text more accurately based on the document's semantic content.
1. Zero-Shot Classification: Finally, the system falls back to zero-shot classification. This utilizes the `facebook/bart-large-mnli` pre-trained model, which can generalize to new document types without any developer efforts.

Note that with enough fine-tuning on Sentence-BERT, the zero-shot classification step can also be removed completely as it is more computationally expensive and useful for more general data.

For the application infrastructure, FastAPI is used as the web framework to handle API requests efficiently and with modern async capabilities. The backend logic and interaction with AI/ML models are implemented in Python. Docker is used to containerize the application, ensuring consistent environments across development, testing, and deployment.

### Extensibility

**File Handling via Registry Pattern**
To support a growing list of file types, the application uses a registry pattern for content extraction. Each supported file extension (e.g., .pdf, .jpg, .docx, .xlsx) maps to a specific extraction function. This modular design allows new file formats to be supported by registering and implementing a new extractor.

**AI/ML Model Adaptability**
The classification logic is built on an AI/ML pipeline, which helps the system generalize to new document categories and industries. As long as labeled example data (real or synthetic) is available, the model can be retrained or fine-tuned to support new industries and document types with minimal refactoring. As an example in this project, support is added for the healthcare industry and health insurance cards.

### Production Readiness

**Docker Containerization**
The application is containerized using Docker, which standardizes setup across development, staging, and production environments. To run a production server, Gunicorn used in the Dockerfile with multiple configurable workers. Docker makes CI/CD integration easier and is compatible with container orchestration services like Kubernetes or cloud platforms like AWS ECS/Fargate for scaling.

**Structured Logging and Request Tracing**
Logging is initialized during application startup using Python’s built-in logging module. Each request is assigned a unique requestId, and all log entries include this ID for traceability. This can allow easier debugging and integration with centralized logging systems like Splunk or AWS CloudWatch.


## Development

Below are the setup steps and prerequisites to be able to run the application and test the service endpoint. CI/CD pipeline is enabled through GitHub Actions and will currently run tests on pushes and pull requests to the `main` branch. Automated tests can be triggered as part of the CI/CD workflow, along with building and deploying the Docker image or other infrastructure. 

### Local Development/Testing
1. Install Python (the project uses Python 3.12)
1. Install Python dependencies:
    ```shell
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```
1. Install other dependencies, commands below are for macOS using [Homebrew](https://brew.sh/):
    ```shell
    brew install tesseract
    brew install opencv
    brew install poppler
    ```
1. Run the Flask app:
    ```shell
    python -m src.app
    ```
1. Test the classifier using a tool like curl:
    ```shell
    curl -X POST -F 'file=@path_to_pdf.pdf' http://127.0.0.1:5000/classify_file
    ```
1. Run tests:
   ```shell
    pytest
    ```
1. Run tests with coverage:
    ```shell
    pytest --cov=src tests/
    ```
1. Generate synthetic data and train classifier
    ```shell
    python scripts/generate_synthetic_data.py
    python scripts/train_classifier.py
    ```

### Run with Docker

1. Install [Docker](https://docs.docker.com/desktop/setup/install/mac-install/)
1. Build Docker image
    ```shell
    docker build -t file-classifier .
    ```
1. Run the Docker container
    ```shell
    docker run -p 8000:8000 file-classifier
    ```
1. Test the classifier using a tool like curl:
    ```shell
    curl -X POST -F 'file=@path_to_pdf.pdf' http://localhost:8000/classify_file
    ```

## Testing

Unit tests were created using `pytest` and `pytest-cov` was used to check for line coverage and core functionality. Manual end-to-end testing was performed for the following cases:
1. Tested all supported filetypes (pdf, png, jpg, docx, xlsx) for the existing document types (bank statement, driver's license, invoice)
1. Tested ambiguous documents to ensure 'unknown' label would be returned
1. Added new industry with `health_insurance_card` as the document type. Tested scripts for generating new synthetic data and updating the classifier. Ensured that new document type was successfully classified
1. Tested case where PDF contains an embedded image and verified the OCR fallback works
1. Tested max content length restriction and validated that oversized files are blocked with a 413 status
1. Tested other invalid inputs (missing file part, disallowed file types, and empty filenames) to confirm error response
1. Confirmed CI/CD workflow is successful through GitHub Actions

Testing is currently limited to core functionality and can be expanded for edge cases and all error scenarios. For production systems, it would be beneficial to have automated integration tests, synthetic tests, and load tests to reduce manual testing efforts and maintain confidence in the system. 


## Future Improvements

1. Scaling
    - Utilize Kubernetes or a cloud container orchestration service to improve scalability, reliability, and ease of deployment. Something like AWS ECS/Fargate can auto scale the services horizontally.
    - Introduce load balancers to handle larger volumes of traffic and also have service health checks to ensure availability
    - Transition to FastAPI, which provides better performance and flexibility for handling asynchronous requests
    - Implement batch file handling with parallel processing to improve efficiency when dealing with large amount of data
    - For ease of deployment and managing infrastructure, implement infrastructure as code (IaC) through tools like Terraform or CDK
    - Depending on traffic patterns, we can also consider a serverless compute architecture (e.g. AWS Lambda) at the cost of longer cold start times
1. Synthetic Data and Model Fine-Tuning
    - Improve the current approach to synthetic data generation and model fine-tuning by integrating more realistic, diverse, and representative datasets.
    - Leverage more real-world examples to make the classifier more robust and accurate in different scenarios.
    - Confidence score thresholds should be adjusted accordingly based on the results with higher-quality data.
1. Flexible Category Management
    - Implement API that allows users to upload an example of a new document type and create a new category
    - This allows more flexible onboarding that is self-service and can be more customizable depending on user needs
1. Security
    - Consider API security by incorporating authentication and authorization mechanisms, such as API keys or OAuth tokens
    - If using cloud services, this can also be accomplished with fine-grained AWS IAM roles and policies
    - Enable rate-limiting and guardrails/input validation to prevent against abuse/attacks
