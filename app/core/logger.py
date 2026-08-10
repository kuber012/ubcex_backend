import logging
import re

SENSITIVE_KEYS = r"(password|token|secret|api_key|authorization|transaction_id)"

class SafeFormatter(logging.Formatter):
    def format(self, record):
        message = super().format(record)
        message = re.sub(
            rf"({SENSITIVE_KEYS}['\"]?\s*[:=]\s*['\"]?)[^'\",\s&]+(['\"]?)",
            r"\1***REDACTED***\2",
            message,
            flags=re.IGNORECASE
        )
        return message

def setup_logging():
    logger = logging.getLogger("ubcex")
    logger.setLevel(logging.INFO)
    
    handler = logging.StreamHandler()
    formatter = SafeFormatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    
    if not logger.handlers:
        logger.addHandler(handler)
        
    return logger

logger = setup_logging()
