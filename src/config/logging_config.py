import logging
from flask import has_request_context, g

class RequestIdFilter(logging.Filter):
    """
    Logging filter to inject `request_id` from Flask's `g` object.
    Fallbacks to 'no-request-id' if outside a request context.
    """
    def filter(self, record):
        if has_request_context() and hasattr(g, 'request_id'):
            record.request_id = g.request_id
        else:
            record.request_id = 'no-request-id'
        return True

class SafeFormatter(logging.Formatter):
    """
    Formatter that ensures `request_id` is always present,
    even if some logs bypass the filter.
    """
    def format(self, record):
        if not hasattr(record, 'request_id'):
            record.request_id = 'no-request-id'
        return super().format(record)

def setup_logging():
    log_format = '%(asctime)s - %(name)s - %(levelname)s - [request_id=%(request_id)s] %(message)s'
    formatter = SafeFormatter(log_format)

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    handler.addFilter(RequestIdFilter())

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(handler)
