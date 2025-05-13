from werkzeug.datastructures import FileStorage

class BaseExtractor:
    def extract(self, file: FileStorage) -> str:
        raise NotImplementedError("Extractor must implement the extract method.")
